# EInvoice SDK contract pin

The three hand-maintained clients implement exactly seven validation-only
machine operations from the immutable catalog bundle dated 2026-10-15:
create/get document; create/get validation operation; get validation result;
list/get validation policy. Issuance, external delivery, and the separate
human Explorer are outside these SDKs.

Source: d0-api-standards commit 4f64277, bundles
einvoice/2026-10-15-console and einvoice/2026-10-15-test.
The canonical public-openapi.json SHA-256 values are:

- console: 0f1b7b1c4f0e8b2fef50e47243518189293dffd207ac2c78740b9a2826ba0cce
- test: 8992eea05febfece436d5125b7db231e19644ef493ab4bb457bfb50ae2ecbdb3

Shared machine authentication source is d0-auth commit 427beab15ee4ba6d6487a85120d920f028a1cee5. Local sibling
source overrides make qualification reproducible within this checked-out
workspace. Before publication, replace them with immutable published Go,
npm and Python package versions; do not publish a package whose dependency
resolves by a relative filesystem path. Neither examples nor tests call live
customer or production endpoints.

The product accepts 16–255-character idempotency keys, while the shared auth
transport accepts at most 128. SDKs enforce the safe 16–128-character
intersection and preserve caller-supplied keys unchanged. Uploads compute the
RFC 9530 SHA-256 Content-Digest from the exact bytes sent. The Node, Go, and
Python HTTP transports set Content-Length for buffered byte bodies. Responses
are bounded at 24 MiB because a valid result can contain up to 1,000 bounded
issues. Polling accepts only caller-selected bounds of at most two minutes and
honors canonical 1–300-second Retry-After hints while remaining cancellable.
