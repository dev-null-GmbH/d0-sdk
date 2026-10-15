# d0 EInvoice TypeScript SDK

Seven validation-only EInvoice operations on one fixed production or customer-test resource. The SDK uses @dev-null-gmbh/auth-machine for OAuth and DPoP. Use separate client IDs and signing keys for production and test.

Create a client with await createEInvoiceClient("test", {clientId, keyId, signingKey, scopes}). Read policies with listValidationPolicies(); upload exact XML bytes with createDocument(xml, stableUploadKey); create a validation with createValidationOperation(documentId, policyId, stableValidationKey); then waitValidation(operationId, 120000). A succeeded operation can have a result with valid=false.

Local qualification uses the reviewed sibling auth source at commit 8cce182:
npm ci --ignore-scripts; npm run check; npm test; npm run example:fixture.
The fixture example executes both profiles through the real product SDK
methods without network access. The file dependency is a development
override. Pin an immutable published auth package before publishing this SDK.
