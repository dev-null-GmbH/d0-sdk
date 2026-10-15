# d0 machine HTTP client for Python

This server-side package handles `client_credentials`, PS256 `private_key_jwt`,
ES256 DPoP, shared token refresh and bounded nonce retries for one organization's
client and one d0 product resource. Product SDKs own their versioned operations,
models, pagination, polling and business error handling.

Use Python 3.14.8 and install from the lockfile with `uv sync --locked`. The shared transport is qualified with the product SDKs. Publication uses the
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

Each request has a 45-second maximum deadline; token exchange has a separate
10-second deadline. Pass `cancel=threading.Event()` to cancel while waiting for a
shared token refresh and between network attempts. An in-flight synchronous
socket call remains bounded by its timeout and may have completed a write when
cancellation is observed; treat that as an uncertain outcome. Concurrent callers
share a refresh but get distinct DPoP proofs. The dedicated TLS 1.3 transport
does not use ambient proxies, cookies or redirect handlers.

Run `uv run --locked python -m unittest discover -s tests -v`, `uv lock --check`,
`uv audit --locked`, and `uv build` from this directory. The fixtures verify real
PS256/ES256 signatures, both nonce paths, exact write replay, origin and header
boundaries, token downgrade, response limits, shared refresh and cancellation.
They are functional checks, not load tests.

Pins were verified on 2026-10-15 against the official
[Python 3.14.8 release](https://www.python.org/downloads/release/python-3148/),
[joserfc 1.7.5 changelog](https://jose.authlib.org/en/changelog/),
[cryptography 50.0.2 documentation](https://cryptography.io/en/50.0.2/), and
[Hatchling release history](https://pypi.org/project/hatchling/).
