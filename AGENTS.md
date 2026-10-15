# d0 SDK distribution

This repository distributes only customer SDKs. Import committed SDK subtrees
through `tools/import_sources.py`; never copy application repositories, secrets,
customer data, or native provider binaries here. `sources.json` pins upstream
commits. `export-manifest.json` records source and transformed file digests.

Maintain the product-specific auth, tenancy, idempotency, exact-money and bounded
retry contracts. Keep registry dependencies exact. Run `tools/check.sh` for SDK
changes. Public publication is a separate release action; do not claim a package
or version exists until its anonymous registry download succeeds.
