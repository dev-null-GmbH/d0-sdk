// Package fixture runs a balanced, unposted Accounting workflow offline.
package fixture

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"

	accounting "github.com/dev-null-GmbH/d0-sdk/accounting/go"
	"github.com/dev-null-GmbH/d0-sdk/accounting/go/gen"
	openapi_types "github.com/oapi-codegen/runtime/types"
)

const suffix = "9GXQ8W5V4R3P2N1M0KJHGF7ED6"
const tenant = "ten_" + suffix

type transport struct {
	Profile accounting.Profile
	Calls   []string
}

func (t *transport) RoundTrip(req *http.Request) (*http.Response, error) {
	resource, _ := t.Profile.Resource()
	if !strings.HasPrefix(req.URL.String(), resource+"/v1/") || req.Header.Get("X-Accounting-Tenant") != tenant {
		return nil, errors.New("fixture profile or tenant crossover")
	}
	key := req.Header.Get("Idempotency-Key")
	if len(key) < 16 {
		return nil, errors.New("fixture missing key")
	}
	t.Calls = append(t.Calls, req.URL.Path)
	var input map[string]any
	if err := json.NewDecoder(req.Body).Decode(&input); err != nil {
		return nil, err
	}
	var output map[string]any
	switch {
	case strings.HasSuffix(req.URL.Path, "/accounts"):
		output = map[string]any{"id": "acct_" + suffix, "accountNo": input["accountNo"], "name": input["name"], "createdAt": "2026-01-01T00:00:00Z"}
	case strings.HasSuffix(req.URL.Path, "/periods"):
		output = map[string]any{"id": "per_" + suffix, "label": input["label"], "startsOn": input["startsOn"], "endsOn": input["endsOn"], "status": "open", "createdAt": "2026-01-01T00:00:00Z"}
	case strings.HasSuffix(req.URL.Path, "/journal-entries"):
		lines, ok := input["lines"].([]any)
		if !ok || len(lines) != 2 {
			return nil, errors.New("fixture requires two lines")
		}
		a := lines[0].(map[string]any)
		b := lines[1].(map[string]any)
		if a["side"] != "debit" || b["side"] != "credit" || a["amount"].(map[string]any)["amount"] != "150000" || b["amount"].(map[string]any)["amount"] != "150000" {
			return nil, errors.New("fixture unbalanced")
		}
		output = map[string]any{"id": "je_" + suffix, "periodId": input["periodId"], "status": "draft", "bookingDate": input["bookingDate"], "currency": "EUR", "lines": lines, "createdAt": "2026-01-01T00:00:00Z"}
	default:
		return nil, errors.New("unexpected fixture route")
	}
	raw, _ := json.Marshal(output)
	return &http.Response{StatusCode: 201, Header: http.Header{"Content-Type": []string{"application/json"}, "Etag": []string{"\"fixture-v1\""}}, Body: io.NopCloser(strings.NewReader(string(raw))), Request: req}, nil
}

// Run returns the opaque draft ID after creating two accounts and one open period.
func Run(profile accounting.Profile) (string, error) {
	mock := &transport{Profile: profile}
	client, err := accounting.NewClient(profile, tenant, &http.Client{Transport: mock})
	if err != nil {
		return "", err
	}
	ctx := context.Background()
	debit, err := client.CreateAccount(ctx, &gen.CreateAccountParams{IdempotencyKey: "fixture-account-00001"}, gen.AccountCreate{AccountNo: "1200", Name: "Bank"})
	if err != nil {
		return "", err
	}
	credit, err := client.CreateAccount(ctx, &gen.CreateAccountParams{IdempotencyKey: "fixture-account-00002"}, gen.AccountCreate{AccountNo: "4000", Name: "Revenue"})
	if err != nil {
		return "", err
	}
	date := func(v string) openapi_types.Date {
		parsed, _ := time.Parse("2006-01-02", v)
		return openapi_types.Date{Time: parsed}
	}
	period, err := client.CreatePeriod(ctx, &gen.CreatePeriodParams{IdempotencyKey: "fixture-period-00001"}, gen.PeriodCreate{Label: "2026-01", StartsOn: date("2026-01-01"), EndsOn: date("2026-01-31")})
	if err != nil {
		return "", err
	}
	amount := gen.Money{Amount: "150000", Currency: "EUR"}
	draft, err := client.CreateJournalEntryDraft(ctx, &gen.CreateJournalEntryDraftParams{IdempotencyKey: "fixture-draft-000001"}, gen.JournalEntryCreate{PeriodId: period.JSON201.Id, BookingDate: date("2026-01-15"), Currency: "EUR", Lines: []gen.JournalLineCreate{{AccountId: debit.JSON201.Id, Side: "debit", Amount: amount}, {AccountId: credit.JSON201.Id, Side: "credit", Amount: amount}}})
	if err != nil {
		return "", err
	}
	if draft.JSON201 == nil || draft.JSON201.Status != gen.Draft || len(mock.Calls) != 4 {
		return "", fmt.Errorf("fixture draft failed")
	}
	return draft.JSON201.Id, nil
}
