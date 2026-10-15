# ERiC Python machine SDK

Use `EricClient.create("production", tenant_uuid, client_id, key_id, signing_key, scopes)` on a trusted server with the shared d0-auth transport. Its 49 named production methods use generated `TypedDict` request/result types; the `"test"` profile exposes only synthetic accepted/rejected simulations. `uv run python examples/fixture.py` exercises both environments offline. `sdk/CONTRACT.md` pins catalog hashes and release prerequisites. The local `d0-auth-machine` dependency is for qualification only; release assembly must pin its immutable public version.
