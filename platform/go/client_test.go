package platform

import (
	"context"
	"encoding/json"
	"io"
	"net/http"
	"strings"
	"testing"

	"github.com/dev-null-GmbH/d0-sdk/platform/go/gen"
	"github.com/oapi-codegen/nullable"
)

type fixtureTransport struct {
	profile Profile
	calls   int
}

func (f *fixtureTransport) RoundTrip(req *http.Request) (*http.Response, error) {
	resource, _ := f.profile.Resource()
	if !strings.HasPrefix(req.URL.String(), resource+"/v1/") {
		panic("profile crossover")
	}
	f.calls++
	status := 200
	var payload any
	switch {
	case req.Method == "GET" && strings.HasSuffix(req.URL.Path, "/domains"):
		payload = map[string]any{"domains": []any{map[string]any{"fqdn": "example.eu", "status": "active", "created_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-01T00:00:00Z"}}}
	case req.Method == "PUT" && strings.HasSuffix(req.URL.Path, "/dns/records/www/A"):
		payload = map[string]any{"name": "www.example.eu", "type": "A", "ttl": 300, "records": []string{"192.0.2.1"}, "read_only": false}
	case req.Method == "GET" && strings.HasSuffix(req.URL.Path, "/dns/records"):
		payload = map[string]any{"records": []any{map[string]any{"name": "www.example.eu", "type": "A", "ttl": 300, "records": []string{"192.0.2.1"}, "read_only": false}}}
	case req.Method == "DELETE" && strings.HasSuffix(req.URL.Path, "/dns/records/www/A"):
		status = 204
	default:
		panic("unexpected fixture route")
	}
	raw, _ := json.Marshal(payload)
	if status == 204 {
		raw = nil
	}
	return &http.Response{StatusCode: status, Header: http.Header{"Content-Type": []string{"application/json"}, "X-Request-Id": []string{"fixture-request"}}, Body: io.NopCloser(strings.NewReader(string(raw))), Request: req}, nil
}
func TestOperationCoverageAndDNSProfiles(t *testing.T) {
	if len(testOperations) != 5 {
		t.Fatalf("test operation count %d", len(testOperations))
	}
	for _, profile := range []Profile{Production, Test} {
		fake := &fixtureTransport{profile: profile}
		sdk, err := NewClient(profile, &http.Client{Transport: fake})
		if err != nil {
			t.Fatal(err)
		}
		ctx := context.Background()
		domains, err := sdk.ListDomains(ctx)
		if err != nil || domains.JSON200 == nil {
			t.Fatalf("%s list: %v", profile, err)
		}
		ttl := int64(300)
		record, err := sdk.UpsertDNSRecord(ctx, "example.eu", "www", "A", gen.RecordUpsertBody{Records: nullable.NewNullableWithValue([]string{"192.0.2.1"}), Ttl: &ttl})
		if err != nil || record.JSON200 == nil || record.JSON200.Name != "www.example.eu" {
			t.Fatalf("%s upsert: %v", profile, err)
		}
		listed, err := sdk.ListDNSRecords(ctx, "example.eu")
		if err != nil || listed.JSON200 == nil {
			t.Fatalf("%s DNS list: %v", profile, err)
		}
		_, err = sdk.DeleteDNSRecord(ctx, "example.eu", "www", "A")
		if err != nil {
			t.Fatal(err)
		}
		if fake.calls != 4 {
			t.Fatalf("%s calls %d", profile, fake.calls)
		}
		if profile == Test {
			if _, err := sdk.GetClusterCatalog(ctx); err == nil || fake.calls != 4 {
				t.Fatal("production operation reached test egress")
			}
		}
	}
}
func TestFixedProfileAndSafeError(t *testing.T) {
	if _, err := NewClient("custom", &http.Client{}); err == nil {
		t.Fatal("custom profile accepted")
	}
	e := &APIError{Status: 409, Type: "conflict", Title: "Conflict"}
	if strings.Contains(e.Error(), "raw secret") {
		t.Fatal("raw error leaked")
	}
	sdk, err := NewClient(Production, &http.Client{Transport: &fixtureTransport{profile: Production}})
	if err != nil {
		t.Fatal(err)
	}
	problem := sdk.problem(409, []byte(`{"type":"conflict","title":"Conflict","detail":"raw secret"}`), &http.Response{Header: http.Header{"Content-Type": []string{"application/problem+json"}, "X-Request-Id": []string{"fixture-request"}}})
	apiError, ok := problem.(*APIError)
	if !ok || apiError.Status != 409 || apiError.RequestID != "fixture-request" || strings.Contains(problem.Error(), "raw secret") {
		t.Fatal("unsafe API error")
	}
}

type auditTransport struct{ calls int }

func (a *auditTransport) RoundTrip(req *http.Request) (*http.Response, error) {
	if req.URL.Host != "api.d0.eu" || req.URL.Path != "/platform/v1/audit/events" {
		panic("audit target crossover")
	}
	if req.URL.Query().Get("limit") != "2" {
		panic("wrong audit limit")
	}
	before := req.URL.Query().Get("before")
	if a.calls == 0 && before != "" {
		panic("first cursor must be absent")
	}
	if a.calls == 1 && before != "older" {
		panic("cursor not forwarded")
	}
	a.calls++
	next := "older"
	if before != "" {
		next = ""
	}
	raw, _ := json.Marshal(map[string]any{"events": []any{}, "next_before": next})
	return &http.Response{StatusCode: 200, Header: http.Header{"Content-Type": []string{"application/json"}}, Body: io.NopCloser(strings.NewReader(string(raw))), Request: req}, nil
}

func TestAuditKeysetAndIdempotencyGuard(t *testing.T) {
	fake := &auditTransport{}
	sdk, err := NewClient(Production, &http.Client{Transport: fake})
	if err != nil {
		t.Fatal(err)
	}
	short := "short"
	_, err = sdk.DeleteCluster(context.Background(), "cl_fixture", &gen.PlatformDeleteClusterParams{IdempotencyKey: short})
	if err == nil || fake.calls != 0 {
		t.Fatal("invalid idempotency key reached transport")
	}
	if _, err := sdk.DeleteCluster(context.Background(), "cl_fixture", nil); err == nil || fake.calls != 0 {
		t.Fatal("missing required key reached transport")
	}
	pages := 0
	next, err := sdk.WalkAuditEvents(context.Background(), 2, 3, "", func([]gen.AuditEventBody) error { pages++; return nil })
	if err != nil || next != "" || pages != 2 || fake.calls != 2 {
		t.Fatalf("audit walk: next=%q pages=%d calls=%d err=%v", next, pages, fake.calls, err)
	}
}
