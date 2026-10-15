import { EInvoiceClient, resourceFor } from "../dist/index.js";

const documentId = "doc_abcdefghijklmnopqrst";
const operationId = "vop_abcdefghijklmnopqrst";
const policyId = "vpol_abcdefghijklmnopqrst";

for (const profile of ["production", "test"]) {
  const transport = {
    async request(target) {
      if (!String(target).startsWith(resourceFor(profile) + "/v1/")) throw new Error("profile crossover");
      const path = new URL(target).pathname;
      let status = 200;
      let body;
      switch (path) {
        case "/einvoice/v1/validation-policies": body = { items: [{ id: policyId }] }; break;
        case "/einvoice/v1/documents": status = 201; body = { id: documentId }; break;
        case "/einvoice/v1/validation-operations": status = 202; body = { id: operationId, status: "queued" }; break;
        case "/einvoice/v1/validation-operations/" + operationId: body = { id: operationId, status: "succeeded" }; break;
        case "/einvoice/v1/validation-operations/" + operationId + "/result": body = { operationId, valid: false, issues: [{ code: "fixture.invalid" }] }; break;
        default: throw new Error("unexpected fixture route");
      }
      return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
    },
  };
  const client = new EInvoiceClient(profile, transport);
  const policies = await client.listValidationPolicies();
  const document = await client.createDocument(new TextEncoder().encode("<synthetic/>"), "fixture-upload-00000001");
  const operation = await client.createValidationOperation(document.id, policies.items[0].id, "fixture-validate-00000001");
  const terminal = await client.waitValidation(operation.id, 2000);
  const result = await client.getValidationResult(terminal.id);
  process.stdout.write(profile + " fixture: operation=" + terminal.id + " valid=" + result.valid + "\n");
}
