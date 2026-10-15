// Package platform is the contract-pinned, machine-only Platform SDK.
package platform

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"regexp"
	"strings"
	"time"

	machine "github.com/dev-null-GmbH/d0-sdk/auth/go"
	"github.com/dev-null-GmbH/d0-sdk/platform/go/gen"
)

type Profile string

const (
	Production Profile = "production"
	Test       Profile = "test"
)

func (p Profile) Resource() (string, error) {
	switch p {
	case Production:
		return "https://api.d0.eu/platform", nil
	case Test:
		return "https://api.test.d0.eu/platform", nil
	default:
		return "", errors.New("unsupported Platform profile")
	}
}

type APIError struct {
	Status                 int
	Type, Title, RequestID string
}

func (e *APIError) Error() string {
	return fmt.Sprintf("Platform request failed (HTTP %d)", e.Status)
}

var safeHeader = regexp.MustCompile(`^[!-~]{1,128}$`)
var safePath = regexp.MustCompile(`^[A-Za-z0-9_.@*-]{1,253}$`)

func validKey(key string) bool {
	return len(key) >= 16 && len(key) <= 128 && safeHeader.MatchString(key)
}
func validPath(value string) bool {
	return value != "." && value != ".." && safePath.MatchString(value)
}

type Client struct {
	profile Profile
	api     *gen.ClientWithResponses
}

type limitedBody struct {
	io.ReadCloser
	remaining int64
}

func (b *limitedBody) Read(p []byte) (int, error) {
	if b.remaining == 0 {
		var one [1]byte
		n, err := b.ReadCloser.Read(one[:])
		if n > 0 {
			return 0, errors.New("Platform response exceeds bound")
		}
		return 0, err
	}
	if int64(len(p)) > b.remaining {
		p = p[:int(b.remaining)]
	}
	n, err := b.ReadCloser.Read(p)
	b.remaining -= int64(n)
	return n, err
}

type boundedTransport struct{ http.RoundTripper }

func (t boundedTransport) RoundTrip(req *http.Request) (*http.Response, error) {
	r, err := t.RoundTripper.RoundTrip(req)
	if err != nil {
		return nil, err
	}
	limit := int64(25_165_824)
	if strings.HasPrefix(r.Header.Get("Content-Type"), "application/octet-stream") || strings.HasPrefix(r.Header.Get("Content-Type"), "application/zip") {
		limit = 536_870_912
	}
	r.Body = &limitedBody{ReadCloser: r.Body, remaining: limit}
	return r, nil
}

// NewMachineClient binds the reviewed OAuth/DPoP transport to exactly one public resource.
func NewMachineClient(profile Profile, config machine.Config) (*Client, error) {
	resource, err := profile.Resource()
	if err != nil {
		return nil, err
	}
	if config.Resource != "" && config.Resource != resource {
		return nil, errors.New("machine resource does not match Platform profile")
	}
	config.Resource = resource
	transport, err := machine.NewClient(config)
	if err != nil {
		return nil, err
	}
	return NewClient(profile, transport)
}

// NewClient accepts a preconfigured shared machine transport; injectable for offline fixtures.
func NewClient(profile Profile, transport *http.Client) (*Client, error) {
	resource, err := profile.Resource()
	if err != nil || transport == nil {
		return nil, errors.New("profile and HTTP client required")
	}
	copy := *transport
	copy.CheckRedirect = func(*http.Request, []*http.Request) error { return http.ErrUseLastResponse }
	baseTransport := copy.Transport
	if baseTransport == nil {
		baseTransport = http.DefaultTransport
	}
	copy.Transport = boundedTransport{baseTransport}
	api, err := gen.NewClientWithResponses(strings.TrimSuffix(resource, "/platform"), gen.WithHTTPClient(&copy))
	if err != nil {
		return nil, err
	}
	return &Client{profile: profile, api: api}, nil
}

func (c *Client) allow(op string) error {
	if c.profile == Test && !testOperations[op] {
		return errors.New("operation unavailable in Platform test environment")
	}
	return nil
}

func (c *Client) problem(status int, raw []byte, response *http.Response) error {
	e := &APIError{Status: status}
	if response != nil {
		id := response.Header.Get("X-Request-ID")
		if safeHeader.MatchString(id) {
			e.RequestID = id
		}
	}
	if len(raw) <= 65536 && (response == nil || strings.HasPrefix(response.Header.Get("Content-Type"), "application/problem+json")) {
		var p struct {
			Type  string `json:"type"`
			Title string `json:"title"`
		}
		if json.Unmarshal(raw, &p) == nil {
			if len(p.Type) <= 256 {
				e.Type = p.Type
			}
			if len(p.Title) <= 256 {
				e.Title = p.Title
			}
		}
	}
	return e
}

// WalkAuditEvents follows the opaque, exclusive next_before cursor for a bounded number of pages.
func (c *Client) WalkAuditEvents(ctx context.Context, limit, maxPages int, before string, visit func([]gen.AuditEventBody) error) (string, error) {
	if limit < 1 || limit > 500 || maxPages < 1 || maxPages > 100 || visit == nil {
		return "", errors.New("audit page limit must be 1..500 and maxPages 1..100")
	}
	for i := 0; i < maxPages; i++ {
		rows := int64(limit)
		params := &gen.PlatformListAuditEventsParams{Limit: &rows}
		if before != "" {
			params.Before = &before
		}
		response, err := c.ListAuditEvents(ctx, params)
		if err != nil {
			return "", err
		}
		if response.JSON200 == nil {
			return "", errors.New("invalid Platform audit response")
		}
		events, _ := response.JSON200.Events.Get()
		if err := visit(events); err != nil {
			return "", err
		}
		next := response.JSON200.NextBefore
		if next == "" {
			return "", nil
		}
		if next == before {
			return "", errors.New("Platform audit cursor did not advance")
		}
		before = next
	}
	return before, nil
}

// Wait polls a caller-selected read operation for at most two minutes. Pass a GET callback and a terminal-state predicate.
func Wait[T any](ctx context.Context, timeout time.Duration, fetch func(context.Context) (T, string, error), terminal func(string) bool) (T, error) {
	var zero T
	if timeout < time.Second || timeout > 2*time.Minute {
		return zero, errors.New("poll timeout must be 1s..2m")
	}
	ctx, cancel := context.WithTimeout(ctx, timeout)
	defer cancel()
	for {
		result, status, err := fetch(ctx)
		if err != nil {
			return zero, err
		}
		if terminal(status) {
			return result, nil
		}
		select {
		case <-ctx.Done():
			return zero, ctx.Err()
		default:
		}
		// Only GET callbacks should be supplied; the bounded context prevents endless polling.
		if err := waitTick(ctx); err != nil {
			return zero, err
		}
	}
}

func waitTick(ctx context.Context) error {
	timer := time.NewTimer(time.Second)
	defer timer.Stop()
	select {
	case <-ctx.Done():
		return ctx.Err()
	case <-timer.C:
		return nil
	}
}
