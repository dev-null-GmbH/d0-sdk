# d0 EInvoice Python SDK

Seven validation-only EInvoice operations on one fixed production or customer-test resource. Authentication, DPoP, nonce retry and redirect blocking come from the shared d0-auth-machine transport. Use separate client IDs and signing keys for production and test.

Create a client with create_client("test", client_id=..., key_id=..., signing_key=..., scopes=[...]). Read policies with list_validation_policies(); upload exact XML bytes with create_document(xml, stable_upload_key); then create_validation_operation(document_id, policy_id, stable_validation_key). wait_validation(operation_id, 120) waits at most two minutes. A succeeded operation can have a result with valid=false.

Local qualification uses the reviewed sibling auth source at commit 8cce182:
uv sync --locked --group dev; uv run python -m unittest discover -s tests;
uv run python examples/fixture.py. The fixture example executes both profiles
through the real product SDK methods without network access. This source path
is a development override. Publish shared auth immutably and replace the
override before publishing this SDK.
