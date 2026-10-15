package einvoice

import (
	"context"
	"crypto/sha256"
	"encoding/base64"
	"errors"
	"io"
	"net/http"
	"strings"
	"sync/atomic"
	"testing"
	"time"

	machine "github.com/dev-null-GmbH/d0-sdk/auth/go"
)

type roundTrip func(*http.Request) (*http.Response, error)

func (fn roundTrip) RoundTrip(r *http.Request) (*http.Response, error) { return fn(r) }
func reply(status int, contentType, body string) *http.Response {
	return &http.Response{StatusCode: status, Header: http.Header{"Content-Type": {contentType}}, Body: io.NopCloser(strings.NewReader(body))}
}

const docID = "doc_abcdefghijklmnopqrst"
const opID = "vop_abcdefghijklmnopqrst"
const policyID = "vpol_abcdefghijklmnopqrst"
const key = "fixture-key-00000001"

func TestProfilesAndAllOperations(t *testing.T) {
	for _, profile := range []Profile{Production, Test} {
		t.Run(string(profile), func(t *testing.T) {
			var calls []string
			resource, _ := profile.Resource()
			transport := &http.Client{Transport: roundTrip(func(r *http.Request) (*http.Response, error) {
				if !strings.HasPrefix(r.URL.String(), resource+"/v1/") {
					t.Fatalf("cross-profile URL: %s", r.URL)
				}
				calls = append(calls, r.Method+" "+r.URL.RequestURI())
				switch r.URL.Path {
				case "/einvoice/v1/documents":
					body, _ := io.ReadAll(r.Body)
					digest := sha256.Sum256(body)
					if r.ContentLength != int64(len(body)) || r.Header.Get("Content-Digest") != "sha-256=:"+base64.StdEncoding.EncodeToString(digest[:])+":" || r.Header.Get("Idempotency-Key") != key {
						t.Fatal("upload lost exact-byte or replay headers")
					}
					return reply(201, "application/json", `{"id":"`+docID+`"}`), nil
				case "/einvoice/v1/documents/" + docID:
					return reply(200, "application/json", `{"id":"`+docID+`"}`), nil
				case "/einvoice/v1/validation-operations":
					body, _ := io.ReadAll(r.Body)
					if string(body) != `{"documentId":"`+docID+`","validationPolicyId":"`+policyID+`"}` || r.Header.Get("Idempotency-Key") != key {
						t.Fatal("validation lost pinned document/policy/key")
					}
					return reply(202, "application/json", `{"id":"`+opID+`","status":"queued"}`), nil
				case "/einvoice/v1/validation-operations/" + opID:
					return reply(200, "application/json", `{"id":"`+opID+`","status":"succeeded"}`), nil
				case "/einvoice/v1/validation-operations/" + opID + "/result":
					return reply(200, "application/json", `{"operationId":"`+opID+`","valid":false,"issues":[{"severity":"error","code":"fixture.invalid","message":"Synthetic"}]}`), nil
				case "/einvoice/v1/validation-policies":
					if r.URL.Query().Get("cursor") != "opaque+cursor" || r.URL.Query().Get("limit") != "7" {
						t.Fatal("policy query changed")
					}
					return reply(200, "application/json", `{"items":[{"id":"`+policyID+`"}]}`), nil
				case "/einvoice/v1/validation-policies/" + policyID:
					return reply(200, "application/json", `{"id":"`+policyID+`"}`), nil
				}
				t.Fatalf("unexpected path %s", r.URL.Path)
				return nil, nil
			})}
			client, err := NewClient(profile, transport)
			if err != nil {
				t.Fatal(err)
			}
			ctx := context.Background()
			if _, err := client.CreateDocument(ctx, []byte("<synthetic/>"), key); err != nil {
				t.Fatal(err)
			}
			if _, err := client.GetDocument(ctx, docID); err != nil {
				t.Fatal(err)
			}
			if _, err := client.CreateValidationOperation(ctx, docID, policyID, key); err != nil {
				t.Fatal(err)
			}
			if _, err := client.GetValidationOperation(ctx, opID); err != nil {
				t.Fatal(err)
			}
			result, err := client.GetValidationResult(ctx, opID)
			if err != nil || result.Valid || len(result.Issues) != 1 {
				t.Fatalf("invalid fixture result: %+v %v", result, err)
			}
			if _, err := client.ListValidationPolicies(ctx, 7, "opaque+cursor"); err != nil {
				t.Fatal(err)
			}
			if _, err := client.GetValidationPolicy(ctx, policyID); err != nil {
				t.Fatal(err)
			}
			if len(calls) != 7 {
				t.Fatalf("expected seven calls, got %d", len(calls))
			}
		})
	}
}

func TestSafeErrorAndBoundedPolling(t *testing.T) {
	if pollDelay([]string{"2"}) != 2*time.Second || pollDelay([]string{"030"}) != time.Second || pollDelay([]string{"301"}) != time.Second {
		t.Fatal("noncanonical retry hint accepted")
	}
	if _, err := NewMachineClient(Test, machine.Config{Resource: "https://api.d0.eu/einvoice"}); err == nil {
		t.Fatal("production machine resource accepted for test profile")
	}
	var count atomic.Int32
	transport := &http.Client{Transport: roundTrip(func(r *http.Request) (*http.Response, error) {
		if strings.HasSuffix(r.URL.Path, "/result") {
			response := reply(409, "application/problem+json", `{"status":409,"type":"https://api.d0.eu/einvoice/problems/result-not-ready","title":"Not ready","detail":"SECRET XML"}`)
			response.Header.Set("X-Request-ID", "request-123")
			return response, nil
		}
		count.Add(1)
		return reply(200, "application/json", `{"id":"`+opID+`","status":"queued"}`), nil
	})}
	client, _ := NewClient(Test, transport)
	_, err := client.GetValidationResult(context.Background(), opID)
	var api *APIError
	if !errors.As(err, &api) || api.Status != 409 || api.RequestID != "request-123" || strings.Contains(err.Error(), "SECRET") {
		t.Fatalf("unsafe error: %v", err)
	}
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	_, err = client.WaitValidation(ctx, opID, 2*time.Second)
	if !errors.Is(err, context.Canceled) {
		t.Fatalf("poll ignored cancellation: %v", err)
	}
	if count.Load() != 0 {
		t.Fatal("cancelled poll sent request")
	}
	_, err = client.WaitValidation(context.Background(), opID, 5*time.Millisecond)
	if !errors.Is(err, context.DeadlineExceeded) || count.Load() == 0 {
		t.Fatalf("poll did not honor its deadline: %v", err)
	}
	if _, err := client.CreateDocument(context.Background(), []byte("<x/>"), "short"); err == nil {
		t.Fatal("unsafe key admitted")
	}
	if _, err := client.GetDocument(context.Background(), "doc_../x"); err == nil {
		t.Fatal("unsafe ID admitted")
	}
}
