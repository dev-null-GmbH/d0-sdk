# d0 machine HTTP client

This Go module owns the common `private_key_jwt` and DPoP transport used by d0
product clients. It uses the fixed issuer `https://auth.d0.eu` and one of the
Platform, Accounting, EInvoice or ERiC production or customer-test resources. Product clients
remain responsible for their versioned operations, models, pagination, polling,
error handling and domain-specific idempotency rules.

```go
client, err := machine.NewClient(machine.Config{
    ClientID: "your-registered-client",
    KeyID: "your-registered-key-id",
    SigningKey: key, // Locally loaded *rsa.PrivateKey, at least 3072 bits.
    Resource: "https://api.d0.eu/platform",
    Scopes: []string{"platform.domains.read"},
})
if err != nil { return err }
defer client.CloseIdleConnections()
request, err := http.NewRequestWithContext(ctx, "GET", "https://api.d0.eu/platform/v1/domains", nil)
if err != nil { return err }
response, err := client.Do(request)
if err != nil { return err }
defer response.Body.Close()
```

The client generates a separate P-256 proof key in memory. Each assertion and
proof receives a fresh identifier. Token and resource nonces have separate
caches. Concurrent requests share a token refresh and receive independent proofs.
Tokens refresh before their five-minute maximum lifetime; requested scopes must
match the issued scopes exactly. Credentials never leave the configured
resource's canonical `/v1` namespace or follow redirects. The dedicated TLS 1.3
transport does not inherit ambient proxy configuration or custom global clients.

For customer testing, register a **separate test OAuth client and grant** with
its own client ID, key ID and private signing key. Select
`https://api.test.d0.eu/platform` and request
`https://api.test.d0.eu/platform/v1/domains` with `platform.domains.read`.
Load the test values separately (for example, `D0_TEST_CLIENT_ID`,
`D0_TEST_KEY_ID`, and `D0_TEST_KEY_FILE`) into the three `Config` fields.
The same test host applies to Accounting, EInvoice and ERiC. Production and
test clients cannot send credentials to each other's API host.

The product SDK and server enforce each operation’s idempotency contract; the
auth transport validates a supplied key but does not classify every POST as a
write. Supply the original `Idempotency-Key` where required and a replayable body:
`http.NewRequestWithContext` supplies `GetBody` automatically for `bytes.Reader`,
`bytes.Buffer` and `strings.Reader`. A custom streaming body must provide its own
`GetBody` that opens the same exact bytes. Preserve the key, body and conditional
headers after an uncertain outcome. The transport retries one nonce challenge,
never a business error or a throttled operation. It returns response statuses
such as `429` and their retry headers to the product client. It does not log or
return the internally added request credentials in `response.Request`.

Run `go test -race ./...` and `go vet ./...` from this directory. The HTTPS
fixtures verify actual PS256 assertions and ES256 proofs, both nonce paths,
request preservation, concurrent token refresh, redirect and origin rejection,
token downgrade, scope/lifetime checks and bounded retries. These are functional
protocol checks, not load tests. The module is source-qualified locally; package
publication and product-client qualification are separate release gates.

Dependency pin verified on 2026-10-15 against the official
[go-jose v4.1.5 release](https://github.com/go-jose/go-jose/releases/tag/v4.1.5).
The implementation uses the library's JOSE signing API and Go's key-generation
APIs; it does not implement signing or token parsing primitives.

The public Go module identity is `github.com/dev-null-GmbH/d0-sdk/auth/go`.
Source ownership remains here; the SDK publication repository mirrors the
qualified package at an immutable release tag. A local source checkout is not
evidence that the public module has been published.
