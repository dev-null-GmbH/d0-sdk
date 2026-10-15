# d0 SDKs

Typed Go, TypeScript and Python clients for d0 Platform, Accounting, EInvoice and
ERiC, with the shared d0 machine OAuth/DPoP transport. These clients are for
trusted server applications. Private signing keys never belong in browser code.

**Release state:** version 0.1.0 is a locally qualified distribution candidate.
Registry publication and live product availability are separate; installation
from the public registries is not claimed yet.

| Product | Production operations | Isolated test operations | Package directories |
| --- | ---: | ---: | --- |
| Shared authentication | OAuth/DPoP transport | Separate resource profiles | [Go](auth/go), [TypeScript](auth/typescript), [Python](auth/python) |
| Platform | 30 | 5 | [Go](platform/go), [TypeScript](platform/typescript), [Python](platform/python) |
| Accounting | 56 | 12 | [Go](accounting/go), [TypeScript](accounting/typescript), [Python](accounting/python) |
| EInvoice | 7 | 7 | [Go](einvoice/go), [TypeScript](einvoice/typescript), [Python](einvoice/python) |
| ERiC | 49 | 2 | [Go](eric/go), [TypeScript](eric/typescript), [Python](eric/python) |

The future registry package names are `@dev-null-gmbh/{product}`,
`d0-{product}` and `github.com/dev-null-GmbH/d0-sdk/{product}/go`.
The auth packages are `@dev-null-gmbh/auth-machine`, `d0-auth-machine` and
`github.com/dev-null-GmbH/d0-sdk/auth/go`. All are pinned to 0.1.0 in this release.

Select `production` or `test` explicitly, use separate client credentials for
each, and grant only the product scopes your integration needs. Each machine
client belongs to one organization; the product client additionally binds its
local tenant/project context. The test profile rejects operations outside its
published allowlist before sending a request. It does not create purchases,
file taxes, post bookkeeping entries or issue invoices.

Authentication handles bounded token refresh, PS256 client assertions and ES256
DPoP. Only an explicit nonce challenge is retried automatically. Product clients
enforce the operation's idempotency and conditional-header requirements. Keep
original keys and request bytes when resolving an uncertain write. Errors expose
bounded technical metadata, not arbitrary response bodies.

Every product includes runnable offline examples in each language's `examples`
directory. They exercise the actual client with a deterministic transport, never
a live service. Contracts and operation inventories are included next to the
clients. API discovery, setup and current product availability belong to the
d0 Developer Console.

## Qualification and provenance

Use Go 1.27.2, Node.js 26.10.0, npm 12.2.0, Python 3.14.8 and uv 0.13.1:

```sh
tools/check.sh
```

This verifies source hashes, all language tests/types, both profile examples,
actual npm archives and Python wheels, and a fresh customer installation.
The Go installation test uses a local module proxy generated from the exact
release source; no private module access or workspace replacement reaches the
customer packages. No load tests are included.

`sources.json` pins the private implementation sources. Only committed SDK
subtrees are imported; `export-manifest.json` records original and distributed
file hashes, including explicit dependency and license metadata adjustments.
Private application code is not part of this repository. Maintainers regenerate
the export with `python3 tools/import_sources.py --sources-root /path/to/checkouts`.
Public CI requires only this repository and public dependencies.

## License

The SDKs and their included documentation are [MIT licensed](LICENSE), copyright
2026 /dev/null GmbH. Dependencies retain their own licenses. This grant applies
to the SDK distribution, not the private product implementations or API service
terms. MIT keeps integration into customers' proprietary applications simple.
Apache 2.0 was considered for its explicit patent grant, but its additional
redistribution requirements are unnecessary for these API client libraries.
See the [MIT text](https://opensource.org/license/mit) and
[Apache 2.0 text](https://www.apache.org/licenses/LICENSE-2.0).

Publication is documented in [PUBLISHING.md](PUBLISHING.md).
