# d0 SDKs

Typed Go, TypeScript and Python clients for d0 Platform, Accounting, EInvoice and
ERiC, with the shared d0 machine OAuth/DPoP transport. These clients are for
trusted server applications. Private signing keys never belong in browser code.

**Release state:** all five Go modules at v0.1.0 are public and verified through
anonymous Go proxy and checksum-database downloads. Accounting and ERiC 0.1.1
are also published and passed fresh anonymous downloads and installed examples.
ERiC 0.1.2 is published with the same verification. All 15 SDK packages are also
available as [qualified release archives](https://github.com/dev-null-GmbH/d0-sdk/releases/tag/sdk-2026-10-15).
GitHub Releases and these public sources are the supported distribution channels.
The SDKs are not published to npm or PyPI; no registry account is needed to install them.
Live product availability is reported separately in the Developer Console.

Accounting 0.1.2 in this source tree is a pending banking release: 80 production
operations, including 24 banking methods, and twelve isolated test operations.
The existing 0.1.1 archives retain their original contents. Publication requires
the exact-commit qualification and anonymous checks in [PUBLISHING.md](PUBLISHING.md).

| Product | Production operations | Isolated test operations | Package directories |
| --- | ---: | ---: | --- |
| Shared authentication | OAuth/DPoP transport | Separate resource profiles | [Go](auth/go), [TypeScript](auth/typescript), [Python](auth/python) |
| Platform | 30 | 5 | [Go](platform/go), [TypeScript](platform/typescript), [Python](platform/python) |
| Accounting | 80 | 12 | [Go](accounting/go), [TypeScript](accounting/typescript), [Python](accounting/python) |
| EInvoice | 7 | 7 | [Go](einvoice/go), [TypeScript](einvoice/typescript), [Python](einvoice/python) |
| ERiC | 49 | 2 | [Go](eric/go), [TypeScript](eric/typescript), [Python](eric/python) |

The package names inside the release archives are `@dev-null-gmbh/{product}`,
`d0-{product}` and `github.com/dev-null-GmbH/d0-sdk/{product}/go`.
The auth packages are `@dev-null-gmbh/auth-machine`, `d0-auth-machine` and
`github.com/dev-null-GmbH/d0-sdk/auth/go`. Auth, Platform and EInvoice use 0.1.0, Accounting uses 0.1.1 and the ERiC
0.1.2 SDK adds the optional filing-consent replay-only header. Product packages
retain the exact auth dependency at 0.1.0.

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

## Install the released packages

Download the [qualified SDK bundle](https://github.com/dev-null-GmbH/d0-sdk/releases/tag/sdk-2026-10-15),
verify its checksum, and unpack it. Run the following in a new directory:

```sh
curl --fail --location --output d0-sdk.zip \
  https://github.com/dev-null-GmbH/d0-sdk/releases/download/sdk-2026-10-15/d0-sdk-2026-10-15.zip
printf '%s  %s\n' \
  6c11b63a5ce5f24dff79d1f3d33c7879ff48831d66dd9029b37abf073152dd93 \
  d0-sdk.zip | shasum -a 256 --check
unzip d0-sdk.zip -d sdk
(cd sdk && shasum -a 256 --check SHA256SUMS)
```

Install the TypeScript packages together so the exact shared authentication
dependency is resolved from the same release. In your application directory,
replace `/absolute/path/to/sdk` with the unpacked directory:

```sh
npm install --ignore-scripts /absolute/path/to/sdk/npm/*.tgz
```

For Python, use your application's virtual environment:

```sh
python -m pip install /absolute/path/to/sdk/python/*.whl
```

Both commands install all five packages; you can instead pass only the auth
archive and the required product archive. Ordinary third-party dependencies
still resolve through the standard package indexes. Go uses public immutable
module tags, for example:

```sh
go get github.com/dev-null-GmbH/d0-sdk/eric/go@v0.1.2
```

The package directories above contain the language-specific API examples.

## Qualification and provenance

Use Go 1.27.3, Node.js 26.10.0, npm 12.2.0, Python 3.14.8 and uv 0.13.1. The combined Python development workspace pins Ruff 0.17.1 to reconcile imported product checks; this does not change runtime package dependencies:

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
