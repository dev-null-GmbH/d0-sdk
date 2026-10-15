package eric

import (
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"io"
	"net/http"
	"os"
	"reflect"
	"strings"
	"testing"
	"time"

	"github.com/dev-null-GmbH/d0-sdk/eric/go/genprod"
	"github.com/dev-null-GmbH/d0-sdk/eric/go/gentest"
	"github.com/google/uuid"
)

const tenant = "11111111-1111-4111-8111-111111111111"
const product = "22222222-2222-4222-8222-222222222222"
const simulation = "33333333-3333-4333-8333-333333333333"

type trip func(*http.Request) (*http.Response, error)

func (f trip) RoundTrip(r *http.Request) (*http.Response, error) { return f(r) }
func response(code int, contentType string, body []byte, headers http.Header) *http.Response {
	if headers == nil {
		headers = make(http.Header)
	}
	headers.Set("Content-Type", contentType)
	return &http.Response{StatusCode: code, Header: headers, Body: io.NopCloser(bytes.NewReader(body)), ContentLength: int64(len(body))}
}
func client(t *testing.T, profile Profile, fn trip) *Client {
	t.Helper()
	c, err := NewClient(profile, tenant, &http.Client{Transport: fn})
	if err != nil {
		t.Fatal(err)
	}
	return c
}
func TestCatalogAndSimulationBoundary(t *testing.T) {
	raw, err := os.ReadFile("../operations.json")
	if err != nil {
		t.Fatal(err)
	}
	var ops []struct{ ID, Profile string }
	if err = json.Unmarshal(raw, &ops); err != nil {
		t.Fatal(err)
	}
	if len(ops) != 51 {
		t.Fatalf("operations=%d", len(ops))
	}
	var prod, test int
	for _, op := range ops {
		if op.Profile == "production" {
			prod++
		} else if op.Profile == "test" {
			test++
		} else {
			t.Fatal(op.Profile)
		}
		method := op.ID
		method = strings.ToUpper(method[:1]) + method[1:]
		if _, ok := reflect.TypeOf(&Client{}).MethodByName(method); !ok {
			t.Fatalf("missing %s", method)
		}
	}
	if prod != 49 || test != 2 {
		t.Fatalf("coverage %d/%d", prod, test)
	}
	calls := 0
	c := client(t, Test, func(r *http.Request) (*http.Response, error) {
		calls++
		if r.URL.Host != "api.test.d0.eu" || r.URL.Path != "/eric/v1/tenants/"+tenant+"/products/"+product+"/simulations" {
			t.Fatalf("wrong test path %s", r.URL)
		}
		if r.Header.Get("X-ERIC-Tenant") != tenant || r.Header.Get("Idempotency-Key") != "fixture-eric-001" {
			t.Fatal("missing bound headers")
		}
		return response(202, "application/json", []byte(`{"id":"`+simulation+`","fixture":"validation-accepted-v1","status":"completed","outcome":"simulated_accepted","simulated":true}`), nil), nil
	})
	_, err = c.GetUserNotices(context.Background(), genprod.ID(product), &genprod.GetUserNoticesParams{})
	if err == nil || calls != 0 {
		t.Fatal("test called production operation")
	}
	ten := uuid.MustParse(tenant)
	p := uuid.MustParse(product)
	result, err := c.CreateEricTestSimulation(context.Background(), ten, p, &gentest.CreateEricTestSimulationParams{IdempotencyKey: "fixture-eric-001"}, gentest.CreateEricTestSimulationJSONRequestBody{Fixture: "validation-accepted-v1"})
	if err != nil {
		t.Fatal(err)
	}
	if result.JSON202 == nil || result.JSON202.Status != "completed" {
		t.Fatal("bad simulation")
	}
	wrong := uuid.MustParse(simulation)
	_, err = c.CreateEricTestSimulation(context.Background(), wrong, p, &gentest.CreateEricTestSimulationParams{IdempotencyKey: "fixture-eric-001"}, gentest.CreateEricTestSimulationJSONRequestBody{Fixture: "validation-rejected-v1"})
	if err == nil || calls != 1 {
		t.Fatal("test tenant mismatch reached transport")
	}
}
func TestProductionReadAndArtifactDigest(t *testing.T) {
	calls := 0
	c := client(t, Production, func(r *http.Request) (*http.Response, error) {
		calls++
		if r.URL.Host != "api.d0.eu" || !strings.HasPrefix(r.URL.Path, "/eric/v1/products/") {
			t.Fatalf("wrong prod route %s", r.URL)
		}
		if r.Header.Get("X-ERIC-Tenant") != tenant {
			t.Fatal("tenant header")
		}
		if strings.HasSuffix(r.URL.Path, "/notices") {
			return response(200, "application/json", []byte(`{"schema_version":"eric.user-notices.v1","version":"fixture","sdk_release":"fixture","documentation_archive_sha256":"digest","license_document_sha256":"digest","license_member":"license","notices":[]}`), nil), nil
		}
		body := []byte("<fixture/>")
		sum := sha256.Sum256(body)
		h := make(http.Header)
		h.Set("Content-Digest", "sha-256=:"+base64.StdEncoding.EncodeToString(sum[:])+":")
		return response(200, "application/xml", body, h), nil
	})
	notices, err := c.GetUserNotices(context.Background(), genprod.ID(product), &genprod.GetUserNoticesParams{})
	if err != nil {
		t.Fatal(err)
	}
	if notices.JSON200 == nil {
		t.Fatal("missing notices")
	}
	a, err := c.GetPreparationArtifact(context.Background(), genprod.ID(product), genprod.ID(simulation), genprod.GetPreparationArtifactParamsKind("payload.xml"), &genprod.GetPreparationArtifactParams{})
	if err != nil {
		t.Fatal(err)
	}
	if string(a.Body) != "<fixture/>" {
		t.Fatal("artifact altered")
	}
	if calls != 2 {
		t.Fatal(calls)
	}
	_, err = c.CreateEricTestSimulation(context.Background(), uuid.MustParse(tenant), uuid.MustParse(product), &gentest.CreateEricTestSimulationParams{}, gentest.CreateEricTestSimulationJSONRequestBody{})
	if err == nil || calls != 2 {
		t.Fatal("prod called test operation")
	}
}
func TestDigestAndBounds(t *testing.T) {
	body := []byte("a")
	sum := sha256.Sum256(body)
	h := make(http.Header)
	h.Set("Content-Digest", "sha-256=:"+base64.StdEncoding.EncodeToString(sum[:])+":")
	h.Set("Content-Length", "1")
	if err := verifyDigest(body, &http.Response{Header: h}, true); err != nil {
		t.Fatal(err)
	}
	h.Set("Content-Length", "2")
	if err := verifyDigest(body, &http.Response{Header: h}, true); err == nil {
		t.Fatal("accepted wrong length")
	}
	h.Set("Content-Length", "1")
	if err := verifyDigest([]byte("b"), &http.Response{Header: h}, true); err == nil {
		t.Fatal("accepted tamper")
	}
	b := &limitedBody{ReadCloser: io.NopCloser(strings.NewReader("abc")), remaining: 2}
	_, err := io.ReadAll(b)
	if err == nil {
		t.Fatal("accepted oversized response")
	}
	if _, err = Wait(context.Background(), 0, func(context.Context) (int, string, error) { return 0, "", nil }, func(string) bool { return true }); err == nil {
		t.Fatal("accepted unbounded poll")
	}
	got, err := Wait(context.Background(), time.Second, func(context.Context) (int, string, error) { return 7, "completed", nil }, func(s string) bool { return s == "completed" })
	if err != nil || got != 7 {
		t.Fatal(got, err)
	}
	if (&APIError{Status: 409}).Error() != "ERiC request failed (HTTP 409)" {
		t.Fatal("unsafe problem")
	}
}

func TestTypedSimulationRejectsMismatchedOutcome(t *testing.T) {
	valid := []byte(`{"id":"33333333-3333-4333-8333-333333333333","fixture":"validation-accepted-v1","status":"completed","outcome":"simulated_accepted","simulated":true}`)
	result, err := parseSimulation(valid)
	if err != nil || result.Outcome != SimulatedAccepted {
		t.Fatal(result, err)
	}
	bad := bytes.Replace(valid, []byte(`"simulated_accepted"`), []byte(`"simulated_rejected"`), 1)
	if _, err := parseSimulation(bad); err == nil {
		t.Fatal("accepted mismatched synthetic outcome")
	}
}
