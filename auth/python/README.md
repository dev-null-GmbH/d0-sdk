# d0 machine HTTP client for Python

This server-side package handles `client_credentials`, PS256 `private_key_jwt`,
ES256 DPoP, shared token refresh and bounded nonce retries for one organization's
client and one d0 product resource. Product SDKs own their versioned operations,
models, pagination, polling and business error handling.

Use Python 3.14.10 and install from the lockfile with `uv sync --locked`. The shared transport is qualified with the product SDKs. Publication uses the
public d0-sdk distribution; a local qualification is not a registry release.

```python
import os
from pathlib import Path

from joserfc.jwk import RSAKey
from d0_auth_machine import MachineClient

key = RSAKey.import_key(Path(os.environ["D0_CLIENT_KEY_FILE"]).read_bytes())
client = MachineClient(
    client_id=os.environ["D0_CLIENT_ID"],
    key_id=os.environ["D0_KEY_ID"],
    signing_key=key,  # Locally held private RSA key, at least 3072 bits.
    resource="https://api.d0.eu/platform",
    scopes=["platform.domains.read"],
)
with client.request("https://api.d0.eu/platform/v1/domains") as response:
    print(response.status, response.read())
```

The resource can be `platform`, `accounting`, `einvoice` or `eric` at
`https://api.d0.eu/<resource>` or `https://api.test.d0.eu/<resource>`.
For customer testing, register a **separate test OAuth client and grant** with
its own client ID, key ID and private signing key. Select
`https://api.test.d0.eu/platform` and request
`https://api.test.d0.eu/platform/v1/domains` with `platform.domains.read`.
Use separate `D0_TEST_CLIENT_ID`, `D0_TEST_KEY_ID`, and `D0_TEST_CLIENT_KEY_FILE`
values for the example's `client_id`, `key_id`, and `signing_key`.
Production and test clients cannot send credentials to each other's API host.
Requests remain under the selected resource's canonical
`/v1` namespace. The issuer is fixed to `https://auth.d0.eu`; private keys,
proofs, tokens and nonces stay in process memory. Only the public client key
belongs in the credential ceremony. The DPoP P-256 key is generated separately
for each client instance.

Use the operation's declared scope and a stable `Idempotency-Key` where its
contract requires one, with an optional `str` or byte body. Product SDKs and
servers enforce that requirement; this auth transport validates a supplied key
and permits read-only POSTs without one. Use the operation's exact method, path, payload
and conditional headers from the product reference; the read-only client above
cannot perform writes.

The client snapshots bytes and headers before authentication, then retries only
one explicit DPoP nonce challenge with new proof material. Preserve the original
key, body and conditional headers after an uncertain write. Business errors,
including `429`, return as ordinary responses. Redirects fail closed. Close or
consume each response. Caller-supplied credentials, cookies, Host overrides and
credential query parameters are rejected.

Each request has a 45-second budget; token exchange shares a separate 10-second
budget across nonce attempts. After connecting, an absolute deadline interrupts
trickled response headers and bodies by shutting down the socket. DNS resolution,
connection setup and TLS negotiation still use standard-library/OS timeouts;
blocking OS DNS resolution cannot be interrupted, so these budgets are not a
strict upper bound on the complete exchange. Token expiry starts before the
network request, so transport delay never extends its cached lifetime.
Pass `cancel=threading.Event()` to cancel while waiting for a shared token refresh
and between network attempts. An in-flight synchronous socket call may have
completed a write when cancellation is observed; treat that as an uncertain
outcome. Concurrent callers share a refresh but get distinct DPoP proofs. The
dedicated TLS 1.3 transport does not use ambient proxies, cookies or redirects.

Run `uv run --locked python -m unittest discover -s tests -v`, `uv lock --check`,
`uv audit --locked`, and `uv build` from this directory. The fixtures verify real
PS256/ES256 signatures, both nonce paths, exact write replay, origin and header
boundaries, token downgrade, response limits, shared refresh and cancellation.
They are functional checks, not load tests. From the repository root, CI runs
the same SDK gate with `docker build --file Dockerfile.python-ci --target python-test --no-cache-filter python-test .`. The image
builds the checksum-pinned official Python source into an isolated prefix and
binds uv to it with automatic interpreter downloads disabled. The test stage
runs afresh, including the vulnerability audit; the source build stays cached. For local checks,
set `UV_PYTHON` to the absolute path of an installed Python 3.14.10 interpreter
when uv cannot discover that patch.

Pins were verified on 2026-10-26 against the official
[Python 3.14.10 security release](https://www.python.org/downloads/release/python-31410/),
[joserfc 1.7.7 changelog](https://jose.authlib.org/en/changelog/),
[cryptography 50.0.2 documentation](https://cryptography.io/en/50.0.2/), and
[Hatchling release history](https://pypi.org/project/hatchling/).
