// Package machine supplies the d0 client-credentials and DPoP HTTP boundary.
package machine

import (
	"context"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/tls"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"slices"
	"strings"
	"sync"
	"time"

	"github.com/go-jose/go-jose/v4"
)

const issuer = "https://auth.d0.eu"

// Config contains one organization's locally held signing key and one resource.
// SigningKey must not be mutated while the client is in use.
type Config struct {
	ClientID, KeyID, Resource string
	Scopes                    []string
	SigningKey                *rsa.PrivateKey
}

// NewClient returns a concurrency-safe client restricted to the resource's /v1
// namespace. Product contracts define idempotency requirements; bodies must be replayable.
// Only nonce challenges are automatically retried; each attempt gets a new proof.
func NewClient(config Config) (*http.Client, error) {
	slash := strings.LastIndex(config.Resource, "/")
	if slash < 0 {
		return nil, errors.New("unsupported d0 resource")
	}
	origin, product := config.Resource[:slash], config.Resource[slash+1:]
	if !slices.Contains([]string{"https://api.d0.eu", "https://api.test.d0.eu"}, origin) || !slices.Contains([]string{"platform", "accounting", "einvoice", "eric"}, product) {
		return nil, errors.New("unsupported d0 resource")
	}
	if !safeValue(config.ClientID, 128) || !safeValue(config.KeyID, 128) || config.SigningKey == nil || config.SigningKey.N == nil || config.SigningKey.N.BitLen() < 3072 || config.SigningKey.Validate() != nil {
		return nil, errors.New("client ID, key ID and valid RSA signing key of at least 3072 bits are required")
	}
	config.Scopes = slices.Clone(config.Scopes)
	slices.Sort(config.Scopes)
	if len(config.Scopes) == 0 || len(config.Scopes) > 64 {
		return nil, errors.New("one to 64 resource scopes are required")
	}
	for i, scope := range config.Scopes {
		if !safeValue(scope, 128) || !strings.HasPrefix(scope, product+".") || (i > 0 && scope == config.Scopes[i-1]) {
			return nil, errors.New("invalid, duplicate or foreign resource scope")
		}
	}
	proof, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		return nil, errors.New("could not create DPoP key")
	}
	network := &http.Transport{TLSClientConfig: &tls.Config{MinVersion: tls.VersionTLS13}, ForceAttemptHTTP2: true,
		TLSHandshakeTimeout: 10 * time.Second, ResponseHeaderTimeout: 30 * time.Second, IdleConnTimeout: 90 * time.Second, MaxIdleConns: 100}
	tr := &transport{config: config, proof: proof, origin: origin, prefix: "/" + product + "/v1", tokenEndpoint: issuer + "/oauth2/token", http: &http.Client{Transport: network}, refresh: make(chan struct{}, 1)}
	return &http.Client{Transport: tr, Timeout: 45 * time.Second, CheckRedirect: func(*http.Request, []*http.Request) error { return http.ErrUseLastResponse }}, nil
}

type transport struct {
	config                        Config
	proof                         *ecdsa.PrivateKey
	origin, prefix, tokenEndpoint string
	http                          *http.Client
	refresh                       chan struct{}
	mu                            sync.Mutex
	token, resourceNonce          string
	expires                       time.Time
	authorizationNonce            string // Protected by refresh, independently of resourceNonce.
}

func safeValue(value string, maximum int) bool {
	if len(value) == 0 || len(value) > maximum {
		return false
	}
	for _, character := range value {
		if character < 0x21 || character > 0x7e {
			return false
		}
	}
	return true
}

func (t *transport) validate(req *http.Request) error {
	if req == nil || req.URL == nil || req.URL.Scheme+"://"+req.URL.Host != t.origin || req.URL.User != nil || req.URL.Fragment != "" || req.URL.RawPath != "" ||
		(req.URL.Path != t.prefix && !strings.HasPrefix(req.URL.Path, t.prefix+"/")) || strings.Contains(req.URL.Path, "//") || strings.Contains(req.URL.Path, "/.") {
		return errors.New("request is outside the configured canonical resource")
	}
	query, err := url.ParseQuery(req.URL.RawQuery)
	if err != nil {
		return errors.New("invalid request query")
	}
	for name := range query {
		if slices.Contains([]string{"access_token", "authorization", "dpop", "client_assertion"}, strings.ToLower(name)) {
			return errors.New("credentials are forbidden in request queries")
		}
	}
	if len(req.Header.Values("Authorization")) != 0 || len(req.Header.Values("DPoP")) != 0 || (req.Host != "" && req.Host != req.URL.Host) {
		return errors.New("caller-provided credentials or Host overrides are forbidden")
	}
	switch req.Method {
	case http.MethodGet, http.MethodHead, http.MethodPost, http.MethodPut, http.MethodPatch, http.MethodDelete:
	default:
		return errors.New("unsupported API method")
	}
	if values := req.Header.Values("Idempotency-Key"); len(values) != 0 && (len(values) != 1 || !safeValue(values[0], 128)) {
		return errors.New("invalid Idempotency-Key")
	}
	if req.Body != nil && req.Body != http.NoBody && req.GetBody == nil {
		return errors.New("authenticated request body must be replayable for a nonce challenge")
	}
	return nil
}

func (t *transport) RoundTrip(req *http.Request) (*http.Response, error) {
	if err := t.validate(req); err != nil {
		if req != nil && req.Body != nil {
			_ = req.Body.Close()
		}
		return nil, err
	}
	token, err := t.accessToken(req.Context())
	if err != nil {
		if req.Body != nil {
			_ = req.Body.Close()
		}
		return nil, err
	}
	for attempt := 0; attempt < 2; attempt++ {
		request := req.Clone(req.Context())
		if attempt > 0 && req.GetBody != nil {
			request.Body, err = req.GetBody()
			if err != nil {
				return nil, errors.New("could not replay request body")
			}
		}
		t.mu.Lock()
		nonce := t.resourceNonce
		t.mu.Unlock()
		proof, err := t.signProof(request.Method, request.URL, nonce, token)
		if err != nil {
			if request.Body != nil {
				_ = request.Body.Close()
			}
			return nil, err
		}
		request.Header.Set("Authorization", "DPoP "+token)
		request.Header.Set("DPoP", proof)
		response, err := t.http.Transport.RoundTrip(request)
		if err != nil {
			if request.Context().Err() != nil {
				return nil, request.Context().Err()
			}
			return nil, errors.New("d0 API transport failed; retry the exact operation and idempotency key if appropriate")
		}
		fresh := responseNonce(response.Header)
		if fresh != "" {
			t.mu.Lock()
			t.resourceNonce = fresh
			t.mu.Unlock()
		}
		if response.StatusCode >= 300 && response.StatusCode < 400 && response.StatusCode != http.StatusNotModified {
			_ = response.Body.Close()
			return nil, errors.New("authenticated API redirects are forbidden")
		}
		if attempt == 0 && response.StatusCode == http.StatusUnauthorized && fresh != "" && nonceChallenge(response.Header) {
			_, _ = io.Copy(io.Discard, io.LimitReader(response.Body, 4096))
			_ = response.Body.Close()
			continue
		}
		// Response.Request would otherwise expose the internally added credentials.
		response.Request = req
		return response, nil
	}
	return nil, errors.New("DPoP nonce retry exhausted")
}

func responseNonce(header http.Header) string {
	values := header.Values("DPoP-Nonce")
	if len(values) == 1 && safeValue(values[0], 512) {
		return values[0]
	}
	return ""
}

func nonceChallenge(header http.Header) bool {
	for _, value := range header.Values("WWW-Authenticate") {
		if strings.HasPrefix(value, "DPoP ") && strings.Contains(value, `error="use_dpop_nonce"`) {
			return true
		}
	}
	return false
}

func (t *transport) accessToken(ctx context.Context) (string, error) {
	t.mu.Lock()
	value, fresh := t.token, time.Until(t.expires) > 30*time.Second
	t.mu.Unlock()
	if fresh {
		return value, nil
	}
	select {
	case t.refresh <- struct{}{}:
		defer func() { <-t.refresh }()
	case <-ctx.Done():
		return "", ctx.Err()
	}
	t.mu.Lock()
	value, fresh = t.token, time.Until(t.expires) > 30*time.Second
	t.mu.Unlock()
	if fresh {
		return value, nil
	}
	return t.fetchToken(ctx)
}

func (t *transport) fetchToken(parent context.Context) (string, error) {
	ctx, cancel := context.WithTimeout(parent, 10*time.Second)
	defer cancel()
	for attempt := 0; attempt < 2; attempt++ {
		now := time.Now()
		assertion, err := sign(jose.PS256, t.config.SigningKey, (&jose.SignerOptions{}).WithType("JWT").WithHeader("kid", t.config.KeyID), map[string]any{
			"iss": t.config.ClientID, "sub": t.config.ClientID, "aud": issuer, "iat": now.Unix(), "exp": now.Add(time.Minute).Unix(), "jti": rand.Text(),
		})
		if err != nil {
			return "", err
		}
		form := url.Values{"grant_type": {"client_credentials"}, "client_assertion_type": {"urn:ietf:params:oauth:client-assertion-type:jwt-bearer"}, "client_assertion": {assertion}, "resource": {t.config.Resource}, "scope": {strings.Join(t.config.Scopes, " ")}}
		request, err := http.NewRequestWithContext(ctx, http.MethodPost, t.tokenEndpoint, strings.NewReader(form.Encode()))
		if err != nil {
			return "", errors.New("invalid token endpoint")
		}
		proof, err := t.signProof("POST", request.URL, t.authorizationNonce, "")
		if err != nil {
			return "", err
		}
		request.Header.Set("Content-Type", "application/x-www-form-urlencoded")
		request.Header.Set("Accept", "application/json")
		request.Header.Set("DPoP", proof)
		response, err := t.http.Transport.RoundTrip(request)
		if err != nil {
			if ctx.Err() != nil {
				return "", ctx.Err()
			}
			return "", errors.New("d0 token transport failed")
		}
		body, err := io.ReadAll(io.LimitReader(response.Body, (32<<10)+1))
		_ = response.Body.Close()
		if err != nil || len(body) > 32<<10 {
			return "", errors.New("invalid token response size")
		}
		fresh := responseNonce(response.Header)
		if fresh != "" {
			t.authorizationNonce = fresh
		}
		if response.StatusCode != http.StatusOK {
			var failure struct{ Error string }
			if attempt == 0 && response.StatusCode == http.StatusBadRequest && fresh != "" && json.Unmarshal(body, &failure) == nil && failure.Error == "use_dpop_nonce" {
				continue
			}
			return "", fmt.Errorf("d0 token request rejected (HTTP %d)", response.StatusCode)
		}
		var result struct {
			AccessToken string `json:"access_token"`
			TokenType   string `json:"token_type"`
			ExpiresIn   int64  `json:"expires_in"`
			Scope       string `json:"scope"`
		}
		if json.Unmarshal(body, &result) != nil || !safeValue(result.AccessToken, 16384) || result.TokenType != "DPoP" || result.ExpiresIn < 1 || result.ExpiresIn > 300 {
			return "", errors.New("invalid DPoP token response")
		}
		scopes := strings.Fields(result.Scope)
		slices.Sort(scopes)
		if !slices.Equal(scopes, t.config.Scopes) {
			return "", errors.New("issued scopes differ from the requested resource scopes")
		}
		t.mu.Lock()
		t.token, t.expires = result.AccessToken, now.Add(time.Duration(result.ExpiresIn)*time.Second)
		t.mu.Unlock()
		return result.AccessToken, nil
	}
	return "", errors.New("authorization nonce retry exhausted")
}

func (t *transport) signProof(method string, target *url.URL, nonce, token string) (string, error) {
	claims := map[string]any{"htm": method, "htu": target.Scheme + "://" + target.Host + target.EscapedPath(), "iat": time.Now().Unix(), "jti": rand.Text()}
	if nonce != "" {
		claims["nonce"] = nonce
	}
	if token != "" {
		hash := sha256.Sum256([]byte(token))
		claims["ath"] = base64.RawURLEncoding.EncodeToString(hash[:])
	}
	return sign(jose.ES256, t.proof, (&jose.SignerOptions{}).WithType("dpop+jwt").WithHeader("jwk", jose.JSONWebKey{Key: &t.proof.PublicKey}), claims)
}

func sign(algorithm jose.SignatureAlgorithm, key any, options *jose.SignerOptions, claims map[string]any) (string, error) {
	signer, err := jose.NewSigner(jose.SigningKey{Algorithm: algorithm, Key: key}, options)
	if err != nil {
		return "", errors.New("could not initialize JWT signer")
	}
	body, err := json.Marshal(claims)
	if err != nil {
		return "", errors.New("could not encode JWT claims")
	}
	signed, err := signer.Sign(body)
	if err != nil {
		return "", errors.New("could not sign JWT")
	}
	compact, err := signed.CompactSerialize()
	if err != nil {
		return "", errors.New("could not serialize JWT")
	}
	return compact, nil
}

func (t *transport) CloseIdleConnections() { t.http.CloseIdleConnections() }
