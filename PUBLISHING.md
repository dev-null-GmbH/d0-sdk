# Publishing SDKs on GitHub

The supported distribution is this public repository, immutable Go module tags,
and qualified package archives in GitHub Releases. npm and PyPI publication is
not part of the current product decision. No npm/PyPI accounts, publisher
configuration, or registry write credentials are required. The active workflow
only qualifies archives and has read-only repository permissions; it never
publishes to those registries.

The repository is the public SDK boundary. Keep application repositories private.
Publish only reviewed exported SDKs, their MIT license, public contracts,
examples, and the distribution tooling already present here.

## Release procedure

1. Merge the reviewed export and require a successful `qualify` job on the exact
   `main` commit. `tools/check.sh` verifies source hashes, package contents,
   language checks, and all twelve product examples installed from packed
   archives in fresh customer directories. Preserve protection of `main` and
   `{auth,platform,accounting,einvoice,eric}/go/v*` tags.
2. Retrieve that successful run's `sdk-<full commit SHA>` artifact as its original
   ZIP through the GitHub Actions artifact API. Verify every entry against its
   internal `SHA256SUMS`, reject unexpected entries, and calculate the ZIP's
   SHA-256. Retain the qualification run, artifact ID, source commit and checksum
   in the release notes. Do not rebuild packages between qualification and
   publication or include application source.
3. On a clean checkout of that qualified commit, run `python3 tools/go_tags.py`
   to check existing module tags. Each existing tag must have exactly the same
   complete module tree. Create missing tags with `--publish` only in the
   documented release context: `GITHUB_REPOSITORY=dev-null-GmbH/d0-sdk`,
   `GITHUB_REF=refs/heads/main`, and `RELEASE_SHA` equal to the checked-out commit.
   The command uses the authenticated `gh` operator session. Never move a tag.
4. Create a GitHub release at the qualified commit with a new `sdk-YYYY-MM-DD`
   tag (or a distinct suffix for another release that day). Upload the original
   ZIP and a checksum file. Use `gh release create --target <commit>` and
   `--notes-file` with the reviewed notes. If a release already exists, inspect
   and verify it; do not overwrite its tag or assets.
5. Download the release ZIP anonymously and compare its byte count, outer
   checksum and all inner checksums. Verify current Go versions with a fresh
   `GOMODCACHE`, `GOPROXY=https://proxy.golang.org`, `GOSUMDB=sum.golang.org`,
   `GOWORK=off`, and empty private-module bypass settings, then run the installed
   product examples. Update the Console's versioned catalog with the exact
   release URL and proven installation commands. A successful build alone is
   not evidence that the public download works.

The retained registry helper scripts are inactive tooling, not a publication
instruction. Enabling another distribution channel requires a new explicit
product decision and its release qualification.

## Current verified release

[SDK release of 15 October 2026](https://github.com/dev-null-GmbH/d0-sdk/releases/tag/sdk-2026-10-15)
contains all 15 language packages from source
`6f2c39612a661ec557e96e5caff093a057e6e1de`, qualified by
[main CI run 38748901791](https://github.com/dev-null-GmbH/d0-sdk/actions/runs/38748901791).
The original artifact ZIP contains 35 package/module files plus `SHA256SUMS`.
Its 404,724-byte anonymous download has SHA-256
`6c11b63a5ce5f24dff79d1f3d33c7879ff48831d66dd9029b37abf073152dd93`.
The README gives direct TypeScript and Python archive installation commands.

Current versions are Auth, Platform and EInvoice 0.1.0, Accounting 0.1.1, and
ERiC 0.1.2. All current Go modules passed anonymous proxy/checksum downloads and
installed examples. Prior tags and release contents remain unchanged. Package
versions come from each product's matching TypeScript/Python metadata; Go uses
the same product version. Source commits and original/exported file hashes
remain in `sources.json` and `export-manifest.json`.

## Verified Accounting banking release

Accounting 0.1.2 imports the source commit pinned in `sources.json`, with
80 production operations and twelve isolated test operations. It adds 24
production banking methods and requires Go 1.27.3. The previous release and
Accounting v0.1.1 module tag remain immutable. Auth and the other product
versions remain unchanged. The [27 October release](https://github.com/dev-null-GmbH/d0-sdk/releases/tag/sdk-2026-10-27)
contains the original qualified artifact from `41cc1bbd8f2823a4f0d97bde76b91184dfab1aad`,
[run 40500893314](https://github.com/dev-null-GmbH/d0-sdk/actions/runs/40500893314),
artifact ID `12732542411`. Its 429529-byte ZIP has SHA-256
`e5647b2949898c36f71ebf4b7c12ad1a8d3a8a503603b605cb4f83ea06e9101f`.
The anonymous download matched that ZIP and all 35 inner checksums. Fresh
TypeScript/Python archive installs and Go proxy/checksum installs ran both
Accounting profile examples and verified the named banking method. The Go
`accounting/go/v0.1.2` tag points at the qualified commit.

The Go patch update is the stable release listed by
[go.dev](https://go.dev/dl/?mode=json), checked on 27 October 2026. The combined
Python development workspace resolves imported Ruff pins through the exact
[Ruff 0.17.1 release](https://github.com/astral-sh/ruff/releases/tag/0.17.1);
runtime package dependencies and other product module trees stay unchanged.
