// Package eric is the contract-pinned, machine-only ERiC SDK.
package eric

import (
	"context"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"regexp"
	"strconv"
	"strings"
	"time"

	machine "github.com/dev-null-GmbH/d0-sdk/auth/go"
	"github.com/dev-null-GmbH/d0-sdk/eric/go/genprod"
	"github.com/dev-null-GmbH/d0-sdk/eric/go/gentest"
	"github.com/google/uuid"
)

type Profile string

const (
	Production Profile = "production"
	Test       Profile = "test"
)

func (p Profile) Resource() (string, error) {
	switch p {
	case Production:
		return "https://api.d0.eu/eric", nil
	case Test:
		return "https://api.test.d0.eu/eric", nil
	default:
		return "", errors.New("unsupported ERiC profile")
	}
}
func (p Profile) Base() (string, error) {
	r, err := p.Resource()
	if err != nil {
		return "", err
	}
	if p == Production {
		return r + "/v1", nil
	}
	return r, nil
}

type APIError struct {
	Status                 int
	Type, Title, RequestID string
}

func (e *APIError) Error() string { return fmt.Sprintf("ERiC request failed (HTTP %d)", e.Status) }

var uuidID = regexp.MustCompile(`^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$`)
var idem = regexp.MustCompile(`^[A-Za-z0-9._:-]{1,128}$`)
var safeHeader = regexp.MustCompile(`^[!-~]{1,128}$`)

type Client struct {
	profile Profile
	tenant  string
	genprod *genprod.ClientWithResponses
	gentest *gentest.ClientWithResponses
}

func NewMachineClient(profile Profile, tenant string, config machine.Config) (*Client, error) {
	resource, err := profile.Resource()
	if err != nil {
		return nil, err
	}
	if config.Resource != "" && config.Resource != resource {
		return nil, errors.New("machine resource does not match ERiC profile")
	}
	config.Resource = resource
	transport, err := machine.NewClient(config)
	if err != nil {
		return nil, err
	}
	return NewClient(profile, tenant, transport)
}

// NewClient accepts a preconfigured shared machine client; injectable for offline fixtures.
func NewClient(profile Profile, tenant string, transport *http.Client) (*Client, error) {
	if _, err := profile.Resource(); err != nil || transport == nil {
		return nil, errors.New("profile and HTTP client required")
	}
	if !uuidID.MatchString(tenant) {
		return nil, errors.New("canonical public tenant UUID required")
	}
	copy := *transport
	copy.CheckRedirect = func(*http.Request, []*http.Request) error { return http.ErrUseLastResponse }
	base := copy.Transport
	if base == nil {
		base = http.DefaultTransport
	}
	copy.Transport = boundedTransport{base}
	editor := func(_ context.Context, r *http.Request) error {
		r.Header.Set("X-ERIC-Tenant", tenant)
		if r.Method != http.MethodGet && r.Method != http.MethodHead && !strings.HasSuffix(r.URL.Path, "/form-plan") && !idem.MatchString(r.Header.Get("Idempotency-Key")) {
			return errors.New("idempotency key must match ERiC contract")
		}
		return nil
	}
	prod, err := genprod.NewClientWithResponses("https://api.d0.eu/eric/v1", genprod.WithHTTPClient(&copy), genprod.WithRequestEditorFn(editor))
	if err != nil {
		return nil, err
	}
	test, err := gentest.NewClientWithResponses("https://api.test.d0.eu/eric", gentest.WithHTTPClient(&copy), gentest.WithRequestEditorFn(editor))
	if err != nil {
		return nil, err
	}
	return &Client{profile: profile, tenant: tenant, genprod: prod, gentest: test}, nil
}

func (c *Client) allow(operation string) error {
	if operation == "createEricTestSimulation" || operation == "getEricTestSimulation" {
		if c.profile != Test {
			return errors.New("simulation unavailable in ERiC production")
		}
		return nil
	}
	if c.profile != Production {
		return errors.New("production operation unavailable in ERiC test environment")
	}
	return nil
}

// Simulation is the deterministic, synthetic-only ERiC test result.
type SimulationFixture string
type SimulationOutcome string

const (
	ValidationAccepted SimulationFixture = "validation-accepted-v1"
	ValidationRejected SimulationFixture = "validation-rejected-v1"
	SimulatedAccepted  SimulationOutcome = "simulated_accepted"
	SimulatedRejected  SimulationOutcome = "simulated_rejected"
)

type Simulation struct {
	ID        uuid.UUID         `json:"id"`
	Fixture   SimulationFixture `json:"fixture"`
	Status    string            `json:"status"`
	Outcome   SimulationOutcome `json:"outcome"`
	Simulated bool              `json:"simulated"`
}

func parseSimulation(body []byte) (Simulation, error) {
	var value Simulation
	if err := json.Unmarshal(body, &value); err != nil {
		return Simulation{}, errors.New("invalid ERiC simulation response")
	}
	accepted := value.Fixture == ValidationAccepted && value.Outcome == SimulatedAccepted
	rejected := value.Fixture == ValidationRejected && value.Outcome == SimulatedRejected
	if value.ID == uuid.Nil || value.Status != "completed" || !value.Simulated || (!accepted && !rejected) {
		return Simulation{}, errors.New("invalid ERiC simulation response")
	}
	return value, nil
}

// Simulate creates one allowed test fixture; it never calls the production API.
func (c *Client) Simulate(ctx context.Context, product uuid.UUID, fixture SimulationFixture, idempotencyKey string) (Simulation, error) {
	if c.profile != Test || (fixture != ValidationAccepted && fixture != ValidationRejected) || !idem.MatchString(idempotencyKey) {
		return Simulation{}, errors.New("invalid ERiC test simulation request")
	}
	selected := uuid.MustParse(c.tenant)
	result, err := c.CreateEricTestSimulation(ctx, selected, product, &gentest.CreateEricTestSimulationParams{IdempotencyKey: idempotencyKey}, gentest.CreateEricTestSimulationJSONRequestBody{Fixture: string(fixture)})
	if err != nil {
		return Simulation{}, err
	}
	return parseSimulation(result.Body)
}

// GetSimulation reads the immutable result of a synthetic test fixture.
func (c *Client) GetSimulation(ctx context.Context, product, simulation uuid.UUID) (Simulation, error) {
	if c.profile != Test {
		return Simulation{}, errors.New("simulation unavailable in ERiC production")
	}
	result, err := c.GetEricTestSimulation(ctx, uuid.MustParse(c.tenant), product, simulation, &gentest.GetEricTestSimulationParams{})
	if err != nil {
		return Simulation{}, err
	}
	return parseSimulation(result.Body)
}

func (c *Client) problem(status int, raw []byte, response *http.Response) error {
	e := &APIError{Status: status}
	if response != nil {
		if id := response.Header.Get("X-Request-ID"); safeHeader.MatchString(id) {
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

func verifyDigest(body []byte, response *http.Response, checkLength bool) error {
	if response == nil {
		return errors.New("missing ERiC artifact response")
	}
	sum := sha256.Sum256(body)
	want := "sha-256=:" + base64.StdEncoding.EncodeToString(sum[:]) + ":"
	values := response.Header.Values("Content-Digest")
	if len(values) != 1 || values[0] != want {
		return errors.New("ERiC artifact Content-Digest mismatch")
	}
	if checkLength {
		values = response.Header.Values("Content-Length")
		if len(values) != 1 {
			return errors.New("missing ERiC artifact Content-Length")
		}
		n, err := strconv.ParseInt(values[0], 10, 64)
		if err != nil || n != int64(len(body)) {
			return errors.New("ERiC artifact Content-Length mismatch")
		}
	}
	return nil
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
			return 0, errors.New("ERiC response exceeds bound")
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

func (t boundedTransport) RoundTrip(r *http.Request) (*http.Response, error) {
	response, err := t.RoundTripper.RoundTrip(r)
	if err != nil {
		return nil, err
	}
	response.Body = &limitedBody{ReadCloser: response.Body, remaining: 41_943_040}
	return response, nil
}

// Wait polls an asynchronous read operation for a caller-selected 1s–2m bound.
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
		tick := time.NewTimer(time.Second)
		select {
		case <-ctx.Done():
			tick.Stop()
			return zero, ctx.Err()
		case <-tick.C:
		}
	}
}
