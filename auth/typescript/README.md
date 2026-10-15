# d0 machine HTTP client for Node.js

The shared client handles `private_key_jwt`, DPoP, token refresh and bounded nonce
retries for one d0 organization and one product resource. Product SDKs own their
versioned operations, models, pagination, polling and business error handling.
Keep this package and private keys on the server; it is not a browser SDK.

```typescript
import { readFile } from "node:fs/promises";
import { importPKCS8 } from "jose";
import { createMachineClient } from "@dev-null-gmbh/auth-machine";

const client = await createMachineClient({
  clientId: process.env.D0_CLIENT_ID!,
  keyId: process.env.D0_KEY_ID!,
  signingKey: await importPKCS8(await readFile(process.env.D0_KEY_FILE!, "utf8"), "PS256"),
  resource: "https://api.d0.eu/platform",
  scopes: ["platform.domains.read"],
});
const response = await client.request("https://api.d0.eu/platform/v1/domains");
if (!response.ok) throw new Error(`API request failed (HTTP ${response.status})`);
const domains = await response.json();
```

Use a locally held RSA key of at least 3072 bits. Only its public key belongs in
the credential ceremony. The library generates a separate in-memory P-256 DPoP
key, uses fresh assertion/proof IDs, separates issuer and API nonces, and shares
concurrent refreshes. The issuer and eight production/customer-test resources are fixed.

For customer testing, register a **separate test OAuth client and grant** with
its own client ID, key ID and private signing key. Select
`https://api.test.d0.eu/platform` and request
`https://api.test.d0.eu/platform/v1/domains` with `platform.domains.read`.
Use separate `D0_TEST_CLIENT_ID`, `D0_TEST_KEY_ID`, and `D0_TEST_KEY_FILE`
values in the example's `clientId`, `keyId`, and `signingKey` fields.
The same test host applies to Accounting, EInvoice and ERiC. Production and
test clients cannot send credentials to each other's API host.

`request` uses Node's standard Fetch implementation. It permits only canonical
HTTPS URLs beneath the selected resource's `/v1` namespace, omits cookies and
referrers, disables caching and never follows redirects. Applications must keep
their Node runtime and trusted network configuration secure. The library does
not accept caller-supplied tokens, proofs, cookies or Host overrides. Private
state uses JavaScript private fields, and transport errors omit request material.

Product SDKs and servers enforce each operation’s idempotency contract. This
auth transport validates a supplied `Idempotency-Key` and permits read-only
POSTs without one. Request bodies are optional strings or byte arrays. Bytes and headers are copied before authentication; both attempts preserve
the key, content and conditional headers. Only a valid nonce challenge receives
one retry. Business errors and `429` responses return to the caller unchanged.
Preserve the original key and bytes after an uncertain write result. Each request
has a 45-second deadline and may receive an `AbortSignal`; token exchange has its
own 10-second deadline. One canceled caller does not cancel another caller's
shared token exchange. Close or consume returned response bodies.

`make machine-typescript-check` at the repository root runs type checks, tests,
build, dependency audit and registry signature checks. Functional fixtures verify
real PS256/ES256 signatures, nonce separation, unchanged retries, concurrent
refresh, token-profile rejection and resource boundaries. Package publication
and each product SDK's qualification are separate release steps.

The exact `jose` 6.2.12 pin was verified against the official
[immutable release](https://github.com/panva/jose/releases/tag/v6.2.12) on
2026-10-15. JOSE operations use that library's signing and key APIs.
