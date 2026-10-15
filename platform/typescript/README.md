# Platform TypeScript machine SDK

Typed named methods for the pinned Platform machine contract, running on a trusted Node server. Supply separate client IDs and signing keys for production and test. The test profile exposes only isolated domain/DNS operations; all other operations fail before egress.

Run `npm run example:fixture` for an offline production/test domain and DNS flow. `PlatformClient.create(profile, config)` constructs the shared auth transport for live use, while `new PlatformClient(profile, transport)` accepts a fixture transport for tests. `*_cents` response fields are exact decimal strings.

The local shared-auth package reference is for source qualification and must be replaced by an immutable published dependency before release.
