# Platform Python machine SDK

Typed methods for the pinned Platform machine contract. Use a server-side d0-auth machine client with a separate client ID and signing key for each `production` or `test` profile. The test profile offers only domain and DNS read/write operations on isolated synthetic data. No purchase, cluster, credential, or staff operation is available there.

Run `uv run python examples/fixture.py` for the complete offline production/test domain and DNS flow. For live calls, `PlatformClient.create(profile, client_id, key_id, signing_key, scopes)` binds the shared transport to the fixed resource. See the shared auth package for local private-key loading; never embed a key in application source.

The local `d0-auth-machine` path override is for source qualification. Publish an immutable auth package before publishing this SDK.
