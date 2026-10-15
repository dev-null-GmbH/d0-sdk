package accounting

import (
	"context"
	"net/http"
	"testing"

	"github.com/dev-null-GmbH/d0-sdk/accounting/go/gen"
)

type denyTransport struct{ called bool }

func (d *denyTransport) RoundTrip(*http.Request) (*http.Response, error) {
	d.called = true
	panic("request must fail before egress")
}

func TestTestProfileFailsClosed(t *testing.T) {
	if len(testOperations) != 12 {
		t.Fatalf("test allowlist has %d operations", len(testOperations))
	}
	transport := &denyTransport{}
	client, err := NewClient(Test, "ten_9GXQ8W5V4R3P2N1M0KJHGF7ED6", &http.Client{Transport: transport})
	if err != nil {
		t.Fatal(err)
	}
	_, err = client.PostJournalEntry(context.Background(), "je_9GXQ8W5V4R3P2N1M0KJHGF7ED6", &gen.PostJournalEntryParams{IdempotencyKey: "fixture-key-00000001"})
	if err == nil || transport.called {
		t.Fatal("production-only posting reached transport")
	}
	for op := range testOperations {
		if err := client.allow(op); err != nil {
			t.Fatalf("%s was blocked: %v", op, err)
		}
	}
	for _, op := range []string{"createDocument", "downloadTenantExport", "createWebhookEndpoint", "postJournalEntry"} {
		if client.allow(op) == nil {
			t.Fatalf("%s allowed in test", op)
		}
	}
}

func TestRequiresPublicTenantAndSafeKey(t *testing.T) {
	if _, err := NewClient(Test, "raw-tenant", &http.Client{}); err == nil {
		t.Fatal("raw tenant accepted")
	}
	client, err := NewClient(Test, "ten_9GXQ8W5V4R3P2N1M0KJHGF7ED6", &http.Client{Transport: &denyTransport{}})
	if err != nil {
		t.Fatal(err)
	}
	_, err = client.CreateAccount(context.Background(), &gen.CreateAccountParams{IdempotencyKey: "short"}, gen.AccountCreate{AccountNo: "1200", Name: "Bank"})
	if err == nil {
		t.Fatal("short idempotency key accepted")
	}
}
