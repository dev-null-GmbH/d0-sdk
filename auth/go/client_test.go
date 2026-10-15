package machine

import (
	"bytes"
	"context"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"net/url"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/go-jose/go-jose/v4"
)

func testConfiguration(t *testing.T) Config {
	t.Helper()
	key, err := rsa.GenerateKey(rand.Reader, 3072)
	if err != nil {
		t.Fatal(err)
	}
	return Config{ClientID: "sdk-fixture", KeyID: "fixture-key", SigningKey: key, Resource: "https://api.d0.eu/platform", Scopes: []string{"platform.domains.read"}}
}

func verifiedClaims(t *testing.T, raw string, algorithm jose.SignatureAlgorithm, key any) (map[string]any, jose.Header) {
	t.Helper()
	signed, err := jose.ParseSigned(raw, []jose.SignatureAlgorithm{algorithm})
	if err != nil || len(signed.Signatures) != 1 {
		t.Fatal("invalid signed JWT", err)
	}
	if key == nil {
		public := signed.Signatures[0].Header.JSONWebKey
		if public == nil || !public.IsPublic() {
			t.Fatal("proof must carry only a public key")
		}
		key = public
	}
	body, err := signed.Verify(key)
	if err != nil {
		t.Fatal("signature verification", err)
	}
	var claims map[string]any
	if err := json.Unmarshal(body, &claims); err != nil {
		t.Fatal(err)
	}
	return claims, signed.Signatures[0].Header
}

func TestNonceRetryPreservesRequestAndSeparatesKeys(t *testing.T) {
	cfg := testConfiguration(t)
	var origin string
	assertions, proofs := map[string]bool{}, map[string]bool{}
	tokens, calls := 0, 0
	server := httptest.NewTLSServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		proof, header := verifiedClaims(t, r.Header.Get("DPoP"), jose.ES256, nil)
		if header.ExtraHeaders["typ"] != "dpop+jwt" || proof["htm"] != r.Method || proof["htu"] != origin+r.URL.Path || proofs[proof["jti"].(string)] {
			t.Error("proof method, URI, type or replay mismatch")
		}
		proofs[proof["jti"].(string)] = true
		if r.URL.Path == "/oauth2/token" {
			tokens++
			if err := r.ParseForm(); err != nil {
				t.Fatal(err)
			}
			claims, assertionHeader := verifiedClaims(t, r.Form.Get("client_assertion"), jose.PS256, &cfg.SigningKey.PublicKey)
			if claims["iss"] != cfg.ClientID || claims["sub"] != cfg.ClientID || claims["aud"] != issuer || claims["exp"].(float64)-claims["iat"].(float64) != 60 || assertionHeader.KeyID != cfg.KeyID || assertions[claims["jti"].(string)] {
				t.Error("invalid or reused client assertion")
			}
			assertions[claims["jti"].(string)] = true
			if r.Form.Get("resource") != cfg.Resource || r.Form.Get("scope") != "platform.domains.read" || r.Form.Get("grant_type") != "client_credentials" || proof["ath"] != nil {
				t.Error("token request changed resource or proof semantics")
			}
			w.Header().Set("DPoP-Nonce", "authorization-nonce")
			if tokens == 1 {
				w.WriteHeader(http.StatusBadRequest)
				_, _ = io.WriteString(w, `{"error":"use_dpop_nonce"}`)
				return
			}
			if proof["nonce"] != "authorization-nonce" {
				t.Error("authorization nonce missing")
			}
			_, _ = io.WriteString(w, `{"access_token":"fixture-token","token_type":"DPoP","expires_in":300,"scope":"platform.domains.read"}`)
			return
		}
		calls++
		body, _ := io.ReadAll(r.Body)
		ath := sha256.Sum256([]byte("fixture-token"))
		if string(body) != `{"unchanged":true}` || r.Header.Get("Idempotency-Key") != "retained-request-key" || r.Header.Get("Authorization") != "DPoP fixture-token" || proof["ath"] != base64.RawURLEncoding.EncodeToString(ath[:]) {
			t.Error("resource request or token hash changed")
		}
		w.Header().Set("DPoP-Nonce", "resource-nonce")
		if calls == 1 {
			w.Header().Set("WWW-Authenticate", `DPoP error="use_dpop_nonce"`)
			w.WriteHeader(http.StatusUnauthorized)
			return
		}
		if proof["nonce"] != "resource-nonce" {
			t.Error("resource nonce mixed with authorization nonce")
		}
		w.WriteHeader(http.StatusCreated)
	}))
	defer server.Close()
	origin = server.URL
	client, err := NewClient(cfg)
	if err != nil {
		t.Fatal(err)
	}
	transport := client.Transport.(*transport)
	transport.tokenEndpoint, transport.origin = origin+"/oauth2/token", origin
	transport.http = server.Client()
	req, _ := http.NewRequestWithContext(t.Context(), http.MethodPost, origin+"/platform/v1/domains?cursor=opaque", bytes.NewBufferString(`{"unchanged":true}`))
	req.Header.Set("Idempotency-Key", "retained-request-key")
	res, err := client.Do(req)
	if err != nil {
		t.Fatal(err)
	}
	_ = res.Body.Close()
	if res.StatusCode != http.StatusCreated || tokens != 2 || calls != 2 || len(assertions) != 2 || len(proofs) != 4 {
		t.Fatalf("nonce flow: status=%d token=%d API=%d", res.StatusCode, tokens, calls)
	}
}

func TestCredentialDestinationAndReplayBoundaries(t *testing.T) {
	client, err := NewClient(testConfiguration(t))
	if err != nil {
		t.Fatal(err)
	}
	for _, target := range []string{"http://api.d0.eu/platform/v1/domains", "https://other.example/platform/v1/domains", "https://api.test.d0.eu/platform/v1/domains", "https://api.d0.eu/accounting/v1/accounts", "https://api.d0.eu/platform/v1/../v1/domains", "https://api.d0.eu/platform/v1/domains?access_token=bad"} {
		req, _ := http.NewRequestWithContext(t.Context(), http.MethodGet, target, nil)
		res, err := client.Do(req)
		if res != nil {
			_ = res.Body.Close()
		}
		if err == nil {
			t.Fatalf("accepted credential destination %s", target)
		}
	}
	req, _ := http.NewRequestWithContext(t.Context(), http.MethodPost, "https://api.d0.eu/platform/v1/domains", strings.NewReader(`{}`))
	req.Header.Set("Idempotency-Key", "")
	res, err := client.Do(req)
	if res != nil {
		_ = res.Body.Close()
	}
	if err == nil {
		t.Fatal("invalid supplied idempotency key accepted")
	}
	req.Header.Set("Idempotency-Key", "stable")
	req.GetBody = nil
	res, err = client.Do(req)
	if res != nil {
		_ = res.Body.Close()
	}
	if err == nil {
		t.Fatal("non-replayable authenticated body accepted")
	}
}

func TestTestResourceSignaturesAndCrossOriginBoundary(t *testing.T) {
	cfg := testConfiguration(t)
	bad := cfg
	bad.Resource = "https://api.preview.d0.eu/platform"
	if _, err := NewClient(bad); err == nil {
		t.Fatal("accepted unlisted resource origin")
	}
	cfg.Resource = "https://api.test.d0.eu/platform"
	client, err := NewClient(cfg)
	if err != nil {
		t.Fatal(err)
	}
	tr := client.Transport.(*transport)
	if tr.origin != "https://api.test.d0.eu" {
		t.Fatal("wrong test resource origin")
	}
	tr.http.Transport = roundTripFunc(func(req *http.Request) (*http.Response, error) {
		proof, _ := verifiedClaims(t, req.Header.Get("DPoP"), jose.ES256, nil)
		if proof["htu"] != req.URL.Scheme+"://"+req.URL.Host+req.URL.Path {
			t.Error("proof target differs from request")
		}
		if req.URL.String() == issuer+"/oauth2/token" {
			body, _ := io.ReadAll(req.Body)
			form, _ := url.ParseQuery(string(body))
			claims, _ := verifiedClaims(t, form.Get("client_assertion"), jose.PS256, &cfg.SigningKey.PublicKey)
			if claims["aud"] != issuer || form.Get("resource") != cfg.Resource {
				t.Error("wrong assertion audience or test resource")
			}
			return &http.Response{StatusCode: 200, Header: make(http.Header), Body: io.NopCloser(strings.NewReader(`{"access_token":"fixture-token","token_type":"DPoP","expires_in":300,"scope":"platform.domains.read"}`))}, nil
		}
		return &http.Response{StatusCode: 204, Header: make(http.Header), Body: http.NoBody}, nil
	})
	req, _ := http.NewRequestWithContext(t.Context(), http.MethodGet, cfg.Resource+"/v1/domains", nil)
	response, err := client.Do(req)
	if err != nil {
		t.Fatal(err)
	}
	_ = response.Body.Close()
	if response.StatusCode != 204 {
		t.Fatal("unexpected API status")
	}
	wrong, _ := http.NewRequestWithContext(t.Context(), http.MethodGet, "https://api.d0.eu/platform/v1/domains", nil)
	if response, err := client.Do(wrong); err == nil {
		_ = response.Body.Close()
		t.Fatal("test client accepted production origin")
	}
}

type roundTripFunc func(*http.Request) (*http.Response, error)

func (f roundTripFunc) RoundTrip(req *http.Request) (*http.Response, error) { return f(req) }

func TestConcurrentRequestsShareOneTokenButFreshProofs(t *testing.T) {
	client, err := NewClient(testConfiguration(t))
	if err != nil {
		t.Fatal(err)
	}
	var mu sync.Mutex
	tokens := 0
	proofs := map[string]bool{}
	server := httptest.NewTLSServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		mu.Lock()
		defer mu.Unlock()
		if r.URL.Path == "/oauth2/token" {
			tokens++
			_, _ = io.WriteString(w, `{"access_token":"fixture-token","token_type":"DPoP","expires_in":300,"scope":"platform.domains.read"}`)
			return
		}
		claims, _ := verifiedClaims(t, r.Header.Get("DPoP"), jose.ES256, nil)
		jti := claims["jti"].(string)
		if proofs[jti] {
			t.Error("concurrent proof replay")
		}
		proofs[jti] = true
		w.WriteHeader(http.StatusNoContent)
	}))
	defer server.Close()
	tr := client.Transport.(*transport)
	tr.tokenEndpoint, tr.origin, tr.http = server.URL+"/oauth2/token", server.URL, server.Client()
	var group sync.WaitGroup
	for range 3 {
		group.Go(func() {
			ctx, cancel := context.WithTimeout(t.Context(), time.Second*5)
			defer cancel()
			req, _ := http.NewRequestWithContext(ctx, http.MethodGet, server.URL+"/platform/v1/domains", nil)
			res, err := client.Do(req)
			if err != nil {
				t.Error(err)
				return
			}
			_ = res.Body.Close()
		})
	}
	group.Wait()
	if tokens != 1 || len(proofs) != 3 {
		t.Fatalf("cache/proofs: tokens=%d proofs=%d", tokens, len(proofs))
	}
}

func TestRejectTokenDowngradeAndBoundRetries(t *testing.T) {
	cfg := testConfiguration(t)
	for _, tc := range []struct {
		name, body string
		status     int
		nonce      string
		wantCalls  int
	}{
		{"bearer downgrade", `{"access_token":"fixture","token_type":"Bearer","expires_in":300,"scope":"platform.domains.read"}`, 200, "", 1},
		{"excess lifetime", `{"access_token":"fixture","token_type":"DPoP","expires_in":301,"scope":"platform.domains.read"}`, 200, "", 1},
		{"wrong scope", `{"access_token":"fixture","token_type":"DPoP","expires_in":300,"scope":"platform.domains.write"}`, 200, "", 1},
		{"oversized response", strings.Repeat("x", (32<<10)+1), 200, "", 1},
		{"nonce loop", `{"error":"use_dpop_nonce"}`, 400, "fresh-nonce", 2},
		{"invalid client no retry", `{"error":"invalid_client"}`, 400, "fresh-nonce", 1},
	} {
		t.Run(tc.name, func(t *testing.T) {
			calls := 0
			server := httptest.NewTLSServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				calls++
				if tc.nonce != "" {
					w.Header().Set("DPoP-Nonce", tc.nonce)
				}
				w.WriteHeader(tc.status)
				_, _ = io.WriteString(w, tc.body)
			}))
			defer server.Close()
			client, err := NewClient(cfg)
			if err != nil {
				t.Fatal(err)
			}
			tr := client.Transport.(*transport)
			tr.tokenEndpoint, tr.http = server.URL+"/oauth2/token", server.Client()
			req, _ := http.NewRequestWithContext(t.Context(), http.MethodGet, cfg.Resource+"/v1/domains", nil)
			response, err := client.Do(req)
			if response != nil {
				_ = response.Body.Close()
			}
			if err == nil || strings.Contains(err.Error(), tc.body) {
				t.Fatal("invalid token accepted or token response exposed")
			}
			if calls != tc.wantCalls {
				t.Fatalf("token attempts: got %d want %d", calls, tc.wantCalls)
			}
		})
	}
}

func TestAuthenticatedRedirectCannotForwardCredentials(t *testing.T) {
	cfg := testConfiguration(t)
	calls := 0
	server := httptest.NewTLSServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		calls++
		w.Header().Set("Location", "/platform/v1/another")
		w.WriteHeader(http.StatusTemporaryRedirect)
	}))
	defer server.Close()
	client, err := NewClient(cfg)
	if err != nil {
		t.Fatal(err)
	}
	tr := client.Transport.(*transport)
	tr.origin, tr.http, tr.token, tr.expires = server.URL, server.Client(), "fixture-token", time.Now().Add(time.Minute)
	req, _ := http.NewRequestWithContext(t.Context(), http.MethodGet, server.URL+"/platform/v1/domains", nil)
	response, err := client.Do(req)
	if response != nil {
		_ = response.Body.Close()
	}
	if err == nil || calls != 1 {
		t.Fatalf("redirect followed or accepted: %v calls=%d", err, calls)
	}
}

func TestIdempotencyRequirementBelongsToProductContract(t *testing.T) {
	client, err := NewClient(testConfiguration(t))
	if err != nil {
		t.Fatal(err)
	}
	tr := client.Transport.(*transport)
	for _, method := range []string{http.MethodPost, http.MethodPut, http.MethodPatch, http.MethodDelete} {
		req, _ := http.NewRequestWithContext(t.Context(), method, "https://api.d0.eu/platform/v1/contract-operation", strings.NewReader(`{}`))
		if err := tr.validate(req); err != nil {
			t.Fatalf("%s without an undeclared key: %v", method, err)
		}
		for _, value := range []string{"", "contains space", strings.Repeat("x", 129)} {
			req.Header.Set("Idempotency-Key", value)
			if err := tr.validate(req); err == nil {
				t.Fatalf("%s accepted invalid supplied key", method)
			}
		}
		req.Header.Set("Idempotency-Key", "original-key")
		if err := tr.validate(req); err != nil {
			t.Fatal(err)
		}
		req.Header.Add("Idempotency-Key", "second-key")
		if err := tr.validate(req); err == nil {
			t.Fatal("duplicate key accepted")
		}
	}
}
