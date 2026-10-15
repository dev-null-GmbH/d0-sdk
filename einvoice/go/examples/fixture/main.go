package main

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"

	einvoice "github.com/dev-null-GmbH/d0-sdk/einvoice/go"
)

// This synthetic transport exercises the real product SDK without network
// access or credentials. The shared machine transport is used for live clients.
type fixture struct{ resource string }

func (f fixture) RoundTrip(r *http.Request) (*http.Response, error) {
	if !strings.HasPrefix(r.URL.String(), f.resource+"/v1/") {
		return nil, fmt.Errorf("profile crossover")
	}
	status, body := 200, "{}"
	switch r.URL.Path {
	case "/einvoice/v1/validation-policies":
		body = `{"items":[{"id":"vpol_abcdefghijklmnopqrst"}]}`
	case "/einvoice/v1/documents":
		status, body = 201, `{"id":"doc_abcdefghijklmnopqrst"}`
	case "/einvoice/v1/validation-operations":
		status, body = 202, `{"id":"vop_abcdefghijklmnopqrst","status":"queued"}`
	case "/einvoice/v1/validation-operations/vop_abcdefghijklmnopqrst":
		body = `{"id":"vop_abcdefghijklmnopqrst","status":"succeeded"}`
	case "/einvoice/v1/validation-operations/vop_abcdefghijklmnopqrst/result":
		body = `{"operationId":"vop_abcdefghijklmnopqrst","valid":false,"issues":[{"severity":"error","code":"fixture.invalid","message":"Synthetic"}]}`
	default:
		return nil, fmt.Errorf("unexpected fixture route")
	}
	return &http.Response{StatusCode: status, Header: http.Header{"Content-Type": {"application/json"}}, Body: io.NopCloser(strings.NewReader(body))}, nil
}

func main() {
	for _, profile := range []einvoice.Profile{einvoice.Production, einvoice.Test} {
		resource, _ := profile.Resource()
		client, err := einvoice.NewClient(profile, &http.Client{Transport: fixture{resource}})
		if err != nil {
			panic(err)
		}
		ctx := context.Background()
		policies, err := client.ListValidationPolicies(ctx, 50, "")
		if err != nil {
			panic(err)
		}
		document, err := client.CreateDocument(ctx, []byte("<synthetic/>"), "fixture-upload-00000001")
		if err != nil {
			panic(err)
		}
		operation, err := client.CreateValidationOperation(ctx, document.ID, policies.Items[0].ID, "fixture-validate-00000001")
		if err != nil {
			panic(err)
		}
		terminal, err := client.WaitValidation(ctx, operation.ID, 2*time.Second)
		if err != nil {
			panic(err)
		}
		result, err := client.GetValidationResult(ctx, terminal.ID)
		if err != nil {
			panic(err)
		}
		fmt.Printf("%s fixture: operation=%s valid=%t\n", profile, terminal.ID, result.Valid)
	}
}
