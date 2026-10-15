// Package einvoice is the seven-operation, validation-only EInvoice client.
// Authentication and DPoP are delegated to the shared d0 machine transport.
package einvoice

import (
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"regexp"
	"strconv"
	"strings"
	"time"

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
		return "https://api.d0.eu/einvoice", nil
	case Test:
		return "https://api.test.d0.eu/einvoice", nil
	default:
		return "", errors.New("unsupported EInvoice profile")
	}
}

// NewMachineClient creates the shared OAuth/DPoP client for exactly one profile.
func NewMachineClient(profile Profile, config machine.Config) (*Client, error) {
	resource, err := profile.Resource()
	if err != nil {
		return nil, err
	}
	if config.Resource != "" && config.Resource != resource {
		return nil, errors.New("machine resource does not match EInvoice profile")
	}
	config.Resource = resource
	transport, err := machine.NewClient(config)
	if err != nil {
		return nil, err
	}
	return NewClient(profile, transport)
}

// NewClient accepts an already configured shared machine client. Its fixed
// profile URLs are independently enforced by that transport before egress.
func NewClient(profile Profile, transport *http.Client) (*Client, error) {
	resource, err := profile.Resource()
	if err != nil || transport == nil {
		return nil, errors.New("profile and HTTP client required")
	}
	copy := *transport
	copy.CheckRedirect = func(*http.Request, []*http.Request) error { return http.ErrUseLastResponse }
	return &Client{base: resource + "/v1", http: &copy}, nil
}

type Client struct {
	base string
	http *http.Client
}
type ByteIdentity struct {
	SizeBytes     int64  `json:"sizeBytes"`
	SHA256        string `json:"sha256"`
	ContentDigest string `json:"contentDigest"`
}
type Document struct {
	Schema       string       `json:"schema"`
	ID           string       `json:"id"`
	MediaType    string       `json:"mediaType"`
	ByteIdentity ByteIdentity `json:"byteIdentity"`
	CreatedAt    string       `json:"createdAt"`
	ExpiresAt    string       `json:"expiresAt"`
}
type ValidationOperation struct {
	Schema             string `json:"schema"`
	ID                 string `json:"id"`
	DocumentID         string `json:"documentId"`
	ValidationPolicyID string `json:"validationPolicyId"`
	Status             string `json:"status"`
	RequestedAt        string `json:"requestedAt"`
	UpdatedAt          string `json:"updatedAt"`
	StartedAt          string `json:"startedAt,omitempty"`
	CompletedAt        string `json:"completedAt,omitempty"`
	ResultID           string `json:"resultId,omitempty"`
	ResultURI          string `json:"resultUri,omitempty"`
	Failure            *struct {
		Code string `json:"code"`
	} `json:"failure,omitempty"`
}
type EvidenceComponent struct {
	Kind                  string `json:"kind"`
	Name                  string `json:"name"`
	Version               string `json:"version"`
	ArtifactSHA256        string `json:"artifactSha256"`
	ArtifactContentDigest string `json:"artifactContentDigest"`
}
type ValidationPolicy struct {
	Schema                string              `json:"schema"`
	ID                    string              `json:"id"`
	Name                  string              `json:"name"`
	Description           string              `json:"description,omitempty"`
	Version               string              `json:"version"`
	Status                string              `json:"status"`
	ManifestSHA256        string              `json:"manifestSha256"`
	ManifestContentDigest string              `json:"manifestContentDigest"`
	AcceptedSyntaxes      []string            `json:"acceptedSyntaxes"`
	Profiles              []string            `json:"profiles"`
	Validator             EvidenceComponent   `json:"validator"`
	Rulesets              []EvidenceComponent `json:"rulesets"`
	PublishedAt           string              `json:"publishedAt"`
}
type PolicyPage struct {
	Schema     string             `json:"schema"`
	Items      []ValidationPolicy `json:"items"`
	NextCursor string             `json:"nextCursor,omitempty"`
}
type ValidationIssue struct {
	Severity string `json:"severity"`
	Code     string `json:"code"`
	Message  string `json:"message"`
	Location string `json:"location,omitempty"`
}
type ValidationResult struct {
	Schema      string `json:"schema"`
	ID          string `json:"id"`
	OperationID string `json:"operationId"`
	Source      struct {
		DocumentID   string       `json:"documentId"`
		MediaType    string       `json:"mediaType"`
		ByteIdentity ByteIdentity `json:"byteIdentity"`
	} `json:"source"`
	ValidationPolicy struct {
		ID                    string `json:"id"`
		Version               string `json:"version"`
		ManifestSHA256        string `json:"manifestSha256"`
		ManifestContentDigest string `json:"manifestContentDigest"`
	} `json:"validationPolicy"`
	Valid       bool   `json:"valid"`
	Syntax      string `json:"syntax"`
	Profile     string `json:"profile,omitempty"`
	ValidatedAt string `json:"validatedAt"`
	Evidence    struct {
		Processor EvidenceComponent   `json:"processor"`
		Validator EvidenceComponent   `json:"validator"`
		Rulesets  []EvidenceComponent `json:"rulesets"`
	} `json:"evidence"`
	Issues []ValidationIssue `json:"issues"`
}

// APIError contains only bounded structural fields. Problem detail and raw
// response bodies are deliberately omitted because they may contain input data.
type APIError struct {
	Status                 int
	Type, Title, RequestID string
}

func (e *APIError) Error() string { return fmt.Sprintf("EInvoice request failed (HTTP %d)", e.Status) }

var idPattern = regexp.MustCompile(`^(?:doc_|vop_|vpol_)[A-Za-z0-9]{20,80}$`)
var keyPattern = regexp.MustCompile(`^[A-Za-z0-9._~:+/=-]{16,128}$`)

func validID(id, prefix string) bool {
	return strings.HasPrefix(id, prefix) && idPattern.MatchString(id)
}
func validKey(key string) bool { return keyPattern.MatchString(key) }

func (c *Client) do(ctx context.Context, method, path, key, media string, body []byte, expected int, out any, retry *time.Duration) error {
	body = bytes.Clone(body)
	request, err := http.NewRequestWithContext(ctx, method, c.base+path, bytes.NewReader(body))
	if err != nil {
		return errors.New("invalid EInvoice request")
	}
	request.Header.Set("Accept", "application/json")
	if key != "" {
		request.Header.Set("Idempotency-Key", key)
	}
	if media != "" {
		request.Header.Set("Content-Type", media)
	}
	if media == "application/xml" {
		digest := sha256.Sum256(body)
		request.Header.Set("Content-Digest", "sha-256=:"+base64.StdEncoding.EncodeToString(digest[:])+":")
	}
	response, err := c.http.Do(request)
	if err != nil {
		if ctx.Err() != nil {
			return ctx.Err()
		}
		return errors.New("EInvoice transport failed; preserve the original idempotency key after an uncertain outcome")
	}
	defer response.Body.Close()
	const maxResponse = 24 << 20
	raw, err := io.ReadAll(io.LimitReader(response.Body, maxResponse+1))
	if err != nil || len(raw) > maxResponse {
		return errors.New("EInvoice response unavailable or oversized")
	}
	if response.StatusCode != expected {
		failure := &APIError{Status: response.StatusCode}
		if requestID := response.Header.Get("X-Request-ID"); len(requestID) <= 128 && requestID != "" && printable(requestID) {
			failure.RequestID = requestID
		}
		var problem struct {
			Type, Title string
			Status      int
		}
		if strings.HasPrefix(response.Header.Get("Content-Type"), "application/problem+json") && json.Unmarshal(raw, &problem) == nil && problem.Status == response.StatusCode {
			if len(problem.Type) <= 2048 && strings.HasPrefix(problem.Type, "https://api.d0.eu/einvoice/problems/") {
				failure.Type = problem.Type
			}
			if len(problem.Title) <= 256 {
				failure.Title = problem.Title
			}
		}
		return failure
	}
	if !strings.HasPrefix(response.Header.Get("Content-Type"), "application/json") || json.Unmarshal(raw, out) != nil {
		return errors.New("invalid EInvoice response")
	}
	if retry != nil {
		*retry = pollDelay(response.Header.Values("Retry-After"))
	}
	return nil
}

func pollDelay(values []string) time.Duration {
	if len(values) != 1 {
		return time.Second
	}
	seconds, err := strconv.Atoi(values[0])
	if err != nil || seconds < 1 || seconds > 300 || strconv.Itoa(seconds) != values[0] {
		return time.Second
	}
	return time.Duration(seconds) * time.Second
}

func printable(value string) bool {
	for _, character := range value {
		if character < '!' || character > '~' {
			return false
		}
	}
	return true
}

func (c *Client) CreateDocument(ctx context.Context, xml []byte, idempotencyKey string) (Document, error) {
	if len(xml) == 0 || len(xml) > 20<<20 || !validKey(idempotencyKey) {
		return Document{}, errors.New("XML bytes or idempotency key invalid")
	}
	var result Document
	err := c.do(ctx, "POST", "/documents", idempotencyKey, "application/xml", xml, 201, &result, nil)
	return result, err
}
func (c *Client) GetDocument(ctx context.Context, id string) (Document, error) {
	if !validID(id, "doc_") {
		return Document{}, errors.New("invalid document ID")
	}
	var result Document
	err := c.do(ctx, "GET", "/documents/"+id, "", "", nil, 200, &result, nil)
	return result, err
}
func (c *Client) CreateValidationOperation(ctx context.Context, documentID, policyID, idempotencyKey string) (ValidationOperation, error) {
	if !validID(documentID, "doc_") || !validID(policyID, "vpol_") || !validKey(idempotencyKey) {
		return ValidationOperation{}, errors.New("validation IDs or idempotency key invalid")
	}
	body, _ := json.Marshal(struct {
		DocumentID         string `json:"documentId"`
		ValidationPolicyID string `json:"validationPolicyId"`
	}{documentID, policyID})
	var result ValidationOperation
	err := c.do(ctx, "POST", "/validation-operations", idempotencyKey, "application/json", body, 202, &result, nil)
	return result, err
}
func (c *Client) GetValidationOperation(ctx context.Context, id string) (ValidationOperation, error) {
	result, _, err := c.getValidationOperation(ctx, id)
	return result, err
}
func (c *Client) getValidationOperation(ctx context.Context, id string) (ValidationOperation, time.Duration, error) {
	if !validID(id, "vop_") {
		return ValidationOperation{}, 0, errors.New("invalid validation operation ID")
	}
	var result ValidationOperation
	var retry time.Duration
	err := c.do(ctx, "GET", "/validation-operations/"+id, "", "", nil, 200, &result, &retry)
	return result, retry, err
}
func (c *Client) GetValidationResult(ctx context.Context, id string) (ValidationResult, error) {
	if !validID(id, "vop_") {
		return ValidationResult{}, errors.New("invalid validation operation ID")
	}
	var result ValidationResult
	err := c.do(ctx, "GET", "/validation-operations/"+id+"/result", "", "", nil, 200, &result, nil)
	return result, err
}
func (c *Client) ListValidationPolicies(ctx context.Context, limit int, cursor string) (PolicyPage, error) {
	if limit < 1 || limit > 100 || len(cursor) > 1024 {
		return PolicyPage{}, errors.New("invalid policy page")
	}
	path := "/validation-policies?limit=" + strconv.Itoa(limit)
	if cursor != "" {
		path += "&cursor=" + url.QueryEscape(cursor)
	}
	var result PolicyPage
	err := c.do(ctx, "GET", path, "", "", nil, 200, &result, nil)
	return result, err
}
func (c *Client) GetValidationPolicy(ctx context.Context, id string) (ValidationPolicy, error) {
	if !validID(id, "vpol_") {
		return ValidationPolicy{}, errors.New("invalid validation policy ID")
	}
	var result ValidationPolicy
	err := c.do(ctx, "GET", "/validation-policies/"+id, "", "", nil, 200, &result, nil)
	return result, err
}

// WaitValidation polls a durable operation until terminal or the supplied
// context/maxWait ends. It never creates another operation or idempotency key.
func (c *Client) WaitValidation(ctx context.Context, id string, maxWait time.Duration) (ValidationOperation, error) {
	if maxWait <= 0 || maxWait > 2*time.Minute {
		return ValidationOperation{}, errors.New("poll limit must be within two minutes")
	}
	ctx, cancel := context.WithTimeout(ctx, maxWait)
	defer cancel()
	for {
		if err := ctx.Err(); err != nil {
			return ValidationOperation{}, err
		}
		operation, retry, err := c.getValidationOperation(ctx, id)
		if err != nil {
			return ValidationOperation{}, err
		}
		switch operation.Status {
		case "succeeded", "failed":
			return operation, nil
		case "queued", "running":
		default:
			return ValidationOperation{}, errors.New("invalid validation state")
		}
		timer := time.NewTimer(retry)
		select {
		case <-ctx.Done():
			if !timer.Stop() {
				<-timer.C
			}
			return ValidationOperation{}, ctx.Err()
		case <-timer.C:
		}
	}
}
