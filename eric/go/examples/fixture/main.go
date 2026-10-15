// Offline ERiC example: production notice read and both test simulations.
package main

import (
	"bytes"
	"context"
	"fmt"
	"io"
	"net/http"
	"strings"

	eric "github.com/dev-null-GmbH/d0-sdk/eric/go"
	"github.com/dev-null-GmbH/d0-sdk/eric/go/genprod"
	"github.com/google/uuid"
)

const tenant = "11111111-1111-4111-8111-111111111111"
const product = "22222222-2222-4222-8222-222222222222"

type fixtureTransport struct{}

func (fixtureTransport) RoundTrip(r *http.Request) (*http.Response, error) {
	var code = 200
	var body string
	switch {
	case strings.HasSuffix(r.URL.Path, "/notices"):
		body = `{"schema_version":"eric.user-notices.v1","version":"fixture","sdk_release":"fixture","documentation_archive_sha256":"digest","license_document_sha256":"digest","license_member":"license","notices":[]}`
	case strings.HasSuffix(r.URL.Path, "/simulations"):
		code = 202
		b, err := io.ReadAll(r.Body)
		if err != nil {
			return nil, err
		}
		fixture := "validation-accepted-v1"
		if bytes.Contains(b, []byte("validation-rejected-v1")) {
			fixture = "validation-rejected-v1"
		}
		outcome := "simulated_accepted"
		if fixture == "validation-rejected-v1" {
			outcome = "simulated_rejected"
		}
		body = fmt.Sprintf(`{"id":"33333333-3333-4333-8333-333333333333","fixture":%q,"status":"completed","outcome":%q,"simulated":true}`, fixture, outcome)
	default:
		return nil, fmt.Errorf("unexpected offline route %s", r.URL.Path)
	}
	h := make(http.Header)
	h.Set("Content-Type", "application/json")
	return &http.Response{StatusCode: code, Header: h, Body: io.NopCloser(strings.NewReader(body))}, nil
}
func main() {
	httpClient := &http.Client{Transport: fixtureTransport{}}
	prod, err := eric.NewClient(eric.Production, tenant, httpClient)
	if err != nil {
		panic(err)
	}
	notice, err := prod.GetUserNotices(context.Background(), genprod.ID(product), &genprod.GetUserNoticesParams{})
	if err != nil || notice.JSON200 == nil {
		panic(fmt.Sprint("notice fixture: ", err))
	}
	test, err := eric.NewClient(eric.Test, tenant, httpClient)
	if err != nil {
		panic(err)
	}
	for _, fixture := range []eric.SimulationFixture{eric.ValidationAccepted, eric.ValidationRejected} {
		result, err := test.Simulate(context.Background(), uuid.MustParse(product), fixture, "offline-eric-001")
		if err != nil || !result.Simulated {
			panic(fmt.Sprint("simulation fixture: ", err))
		}
	}
	fmt.Println("ERiC production read-only + both test simulations: offline fixtures passed")
}
