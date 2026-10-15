// Package accounting is the contract-pinned, machine-only Accounting SDK.
package accounting

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

	"github.com/dev-null-GmbH/d0-sdk/accounting/go/gen"
	machine "github.com/dev-null-GmbH/d0-sdk/auth/go"
)

type Profile string

const (
	Production Profile = "production"
	Test       Profile = "test"
)

func (p Profile) Resource() (string, error) {
	switch p {
	case Production:
		return "https://api.d0.eu/accounting", nil
	case Test:
		return "https://api.test.d0.eu/accounting", nil
	default:
		return "", errors.New("unsupported Accounting profile")
	}
}

type APIError struct {
	Status                 int
	Type, Title, RequestID string
}

func (e *APIError) Error() string {
	return fmt.Sprintf("Accounting request failed (HTTP %d)", e.Status)
}

var tenantID = regexp.MustCompile(`^ten_[0-9A-HJKMNP-TV-Z]{26}$`)
var safeHeader = regexp.MustCompile(`^[!-~]{1,128}$`)

type Client struct {
	profile Profile
	tenant  string
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
			return 0, errors.New("Accounting response exceeds bound")
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
func NewMachineClient(profile Profile, tenant string, config machine.Config) (*Client, error) {
	resource, err := profile.Resource()
	if err != nil {
		return nil, err
	}
	if config.Resource != "" && config.Resource != resource {
		return nil, errors.New("machine resource does not match Accounting profile")
	}
	config.Resource = resource
	transport, err := machine.NewClient(config)
	if err != nil {
		return nil, err
	}
	return NewClient(profile, tenant, transport)
}

// NewClient accepts a preconfigured shared machine transport; injectable for offline fixtures.
// An empty tenant is allowed solely for listTenants/createTenant onboarding.
func NewClient(profile Profile, tenant string, transport *http.Client) (*Client, error) {
	resource, err := profile.Resource()
	if err != nil || transport == nil {
		return nil, errors.New("profile and HTTP client required")
	}
	if tenant != "" && !tenantID.MatchString(tenant) {
		return nil, errors.New("invalid public tenant ID")
	}
	copy := *transport
	copy.CheckRedirect = func(*http.Request, []*http.Request) error { return http.ErrUseLastResponse }
	baseTransport := copy.Transport
	if baseTransport == nil {
		baseTransport = http.DefaultTransport
	}
	copy.Transport = boundedTransport{baseTransport}
	api, err := gen.NewClientWithResponses(resource+"/v1", gen.WithHTTPClient(&copy), gen.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
		if tenant != "" {
			req.Header.Set("X-Accounting-Tenant", tenant)
		}
		if req.Method != http.MethodGet && req.Method != http.MethodHead {
			key := req.Header.Get("Idempotency-Key")
			if len(key) < 16 || len(key) > 128 || !safeHeader.MatchString(key) {
				return errors.New("idempotency key must be 16–128 safe characters")
			}
		}
		return nil
	}))
	if err != nil {
		return nil, err
	}
	return &Client{profile: profile, tenant: tenant, api: api}, nil
}

func (c *Client) allow(op string) error {
	if c.tenant == "" && op != "listTenants" && op != "createTenant" {
		return errors.New("selected public tenant ID required")
	}
	if c.profile == Test && !testOperations[op] {
		return errors.New("operation unavailable in Accounting test environment")
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

// WalkPages follows opaque cursors for at most maxPages, visiting one page at a time.
func WalkPages[T any](ctx context.Context, limit, maxPages int, after string, fetch func(context.Context, int, string) ([]T, string, error), visit func([]T) error) (string, error) {
	if limit < 1 || limit > 100 || maxPages < 1 || maxPages > 100 {
		return "", errors.New("page limit and maxPages must be 1..100")
	}
	for i := 0; i < maxPages; i++ {
		items, next, err := fetch(ctx, limit, after)
		if err != nil {
			return "", err
		}
		if err := visit(items); err != nil {
			return "", err
		}
		if next == "" {
			return "", nil
		}
		if next == after {
			return "", errors.New("Accounting cursor did not advance")
		}
		after = next
	}
	return after, nil
}

// Wait polls a caller-selected read operation for at most two minutes. It never posts money.
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

// Download is deliberately streaming for binary export/document responses.
func ReadBinary(r io.Reader, max int64) ([]byte, error) {
	if max <= 0 {
		return nil, errors.New("positive response bound required")
	}
	b, err := io.ReadAll(io.LimitReader(r, max+1))
	if err != nil {
		return nil, err
	}
	if int64(len(b)) > max {
		return nil, errors.New("response exceeds bound")
	}
	return b, nil
}
