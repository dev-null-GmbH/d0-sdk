# d0 EInvoice Go SDK

Seven validation-only EInvoice operations on one fixed production or customer-test resource. NewMachineClient delegates OAuth and DPoP to the shared d0-auth/packages/machine/go transport. Use separate client IDs and signing keys for production and test.

Pass machine.Config with the local signing key, client ID, key ID, and EInvoice scopes to NewMachineClient(Test, config). Read policies with ListValidationPolicies, upload exact XML bytes with CreateDocument, create a validation with CreateValidationOperation, and WaitValidation for at most two minutes. A succeeded operation can have a result with valid=false.

Local qualification: go test -race ./... and go run ./examples/fixture. The
example executes the complete synthetic workflow for both profiles through
the real product SDK methods without network access. The relative replace
uses the reviewed sibling shared-auth source at commit 8cce182. Replace it
with an immutable published module version before publishing this SDK.
