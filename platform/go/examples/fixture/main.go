package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"

	platform "github.com/dev-null-GmbH/d0-sdk/platform/go"
	"github.com/dev-null-GmbH/d0-sdk/platform/go/gen"
	"github.com/oapi-codegen/nullable"
)

type fixture struct{ profile platform.Profile }

func (f fixture) RoundTrip(req *http.Request) (*http.Response, error) {
	resource, _ := f.profile.Resource()
	if !strings.HasPrefix(req.URL.String(), resource+"/v1/") {
		return nil, fmt.Errorf("profile crossover")
	}
	var data any
	switch {
	case req.Method == "GET" && strings.HasSuffix(req.URL.Path, "/domains"):
		data = map[string]any{"domains": []any{map[string]any{"fqdn": "example.eu", "status": "active", "created_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-01T00:00:00Z"}}}
	case req.Method == "PUT" && strings.HasSuffix(req.URL.Path, "/dns/records/www/A"):
		data = map[string]any{"name": "www.example.eu", "type": "A", "ttl": 300, "records": []string{"192.0.2.1"}, "read_only": false}
	default:
		return nil, fmt.Errorf("unexpected route")
	}
	raw, _ := json.Marshal(data)
	return &http.Response{StatusCode: 200, Header: http.Header{"Content-Type": []string{"application/json"}}, Body: io.NopCloser(strings.NewReader(string(raw))), Request: req}, nil
}
func main() {
	for _, profile := range []platform.Profile{platform.Production, platform.Test} {
		sdk, err := platform.NewClient(profile, &http.Client{Transport: fixture{profile}})
		if err != nil {
			panic(err)
		}
		domains, err := sdk.ListDomains(context.Background())
		if err != nil || domains.JSON200 == nil {
			panic("list failed")
		}
		got, _ := domains.JSON200.Domains.Get()
		record, err := sdk.UpsertDNSRecord(context.Background(), got[0].Fqdn, "www", "A", gen.RecordUpsertBody{Records: nullable.NewNullableWithValue([]string{"192.0.2.1"})})
		if err != nil || record.JSON200 == nil {
			panic("upsert failed")
		}
		fmt.Printf("%s: %s\n", profile, record.JSON200.Name)
	}
}
