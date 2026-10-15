# Publishing 0.1.0

The repository is the public SDK boundary. Do not change any application
repository's visibility. Publish only reviewed exported SDK files, the license,
public contracts, examples and distribution tooling in this repository.

1. Create `dev-null-GmbH/d0-sdk` as a public repository, push the reviewed main
   commit, and require its qualification job for changes. Protect main and the
   five `{auth,platform,accounting,einvoice,eric}/go/v0.1.0` tags from replacement.
2. Configure npm ownership of `@dev-null-gmbh` and the five package names.
   Configure each trusted publisher for owner `dev-null-GmbH`, repository
   `d0-sdk`, workflow `release.yml`, environment `public-sdk-release`, with
   direct `npm publish` allowed. Initial npm package creation may need the
   organization's authenticated bootstrap before a publisher can be assigned.
   Do not create a long-lived write token for CI.
3. Configure the five PyPI projects (or pending publishers) with those same
   GitHub repository/workflow/environment claims. Keep publisher administration
   with the company's package owners.
4. Run `Qualify and publish SDKs` on main with `publish=true`. The qualification
   job has no publishing authority. The publishing job downloads only that run's
   qualified archives, checks their digests, publishes auth before product
   packages and obtains registry credentials through OIDC. Existing identical
   versions can resume; different bytes at the same version fail closed. No
   customer or API requests are sent by this workflow.
5. The tag job creates all five immutable Go module tags at the same source
   commit. The final job verifies anonymous registry downloads and runs all
   product examples from installed packages. After it succeeds,
   update the Console SDK catalog's publication evidence and this release state.
   A successful build alone is not evidence that registries serve the package.

The workflow retains npm/Python artifacts and a Go module-proxy fixture with
SHA-256 checksums. Upstream source commits and original/exported file hashes
remain committed in `sources.json` and `export-manifest.json`.

Qualification uses exact existing product tool versions; download-artifact
v8.0.2 was additionally verified against its official release on 2026-10-15.
Registry integration follows [npm trusted publishing](https://docs.npmjs.com/trusted-publishers/),
[PyPI trusted publishing](https://docs.pypi.org/trusted-publishers/), and
[uv publishing](https://docs.astral.sh/uv/guides/package/).
