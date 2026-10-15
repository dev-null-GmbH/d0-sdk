import { createHash } from "node:crypto";
import { describe, expect, it, vi } from "vitest";
import type { MachineClient, MachineRequest } from "@dev-null-gmbh/auth-machine";
import { APIError, EInvoiceClient, resourceFor } from "./index.js";

const documentID = "doc_abcdefghijklmnopqrst";
const operationID = "vop_abcdefghijklmnopqrst";
const policyID = "vpol_abcdefghijklmnopqrst";
const key = "fixture-key-00000001";

function response(status: number, body: unknown, media = "application/json"): Response {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": media } });
}

describe("seven fixed EInvoice operations", () => {
  for (const profile of ["production", "test"] as const) {
    it("uses " + profile + " resource and exact upload bytes", async () => {
      const urls: string[] = [];
      const transport: MachineClient = {
        async request(target: string | URL, options: MachineRequest = {}) {
          const url = String(target);
          expect(url.startsWith(resourceFor(profile) + "/v1/")).toBe(true);
          urls.push(url);
          const path = new URL(url).pathname;
          const headers = new Headers(options.headers);
          if (path === "/einvoice/v1/documents") {
            const body = options.body as Uint8Array;
            expect(headers.get("Content-Digest")).toBe(
              "sha-256=:" + createHash("sha256").update(body).digest("base64") + ":",
            );
            expect(headers.get("Idempotency-Key")).toBe(key);
            return response(201, { id: documentID });
          }
          if (path === "/einvoice/v1/documents/" + documentID) return response(200, { id: documentID });
          if (path === "/einvoice/v1/validation-operations") {
            expect(JSON.parse(new TextDecoder().decode(options.body as Uint8Array))).toEqual({
              documentId: documentID, validationPolicyId: policyID,
            });
            expect(headers.get("Idempotency-Key")).toBe(key);
            return response(202, { id: operationID, status: "queued" });
          }
          if (path === "/einvoice/v1/validation-operations/" + operationID) return response(200, { id: operationID, status: "succeeded" });
          if (path === "/einvoice/v1/validation-operations/" + operationID + "/result") return response(200, { operationId: operationID, valid: false, issues: [{ code: "fixture.invalid" }] });
          if (path === "/einvoice/v1/validation-policies") {
            expect(new URL(url).searchParams.get("cursor")).toBe("opaque+cursor");
            return response(200, { items: [{ id: policyID }] });
          }
          if (path === "/einvoice/v1/validation-policies/" + policyID) return response(200, { id: policyID });
          throw new Error("unexpected route");
        },
      };
      const client = new EInvoiceClient(profile, transport);
      expect((await client.createDocument(new TextEncoder().encode("<synthetic/>"), key)).id).toBe(documentID);
      expect((await client.getDocument(documentID)).id).toBe(documentID);
      expect((await client.createValidationOperation(documentID, policyID, key)).id).toBe(operationID);
      expect((await client.getValidationOperation(operationID)).status).toBe("succeeded");
      expect((await client.getValidationResult(operationID)).valid).toBe(false);
      expect((await client.listValidationPolicies(7, "opaque+cursor")).items[0]?.id).toBe(policyID);
      expect((await client.getValidationPolicy(policyID)).id).toBe(policyID);
      expect(urls).toHaveLength(7);
    });
  }

  it("rejects unsafe IDs and keys, keeps errors structural, and cancels polling", async () => {
    let calls = 0;
    const transport: MachineClient = {
      async request() {
        calls++;
        return response(409, {
          status: 409, type: "https://api.d0.eu/einvoice/problems/result-not-ready",
          title: "Not ready", detail: "SECRET XML",
        }, "application/problem+json");
      },
    };
    const client = new EInvoiceClient("test", transport);
    expect(() => client.getDocument("doc_../x")).toThrow();
    expect(() => client.createDocument(new Uint8Array([1]), "short")).toThrow();
    const abort = new AbortController();
    abort.abort();
    await expect(client.waitValidation(operationID, 2000, abort.signal)).rejects.toBeDefined();
    expect(calls).toBe(0);
    const queued: MachineClient = { async request() { return response(200, { id: operationID, status: "queued" }); } };
    await expect(new EInvoiceClient("test", queued).waitValidation(operationID, 5)).rejects.toBeDefined();
    await expect(client.getValidationResult(operationID)).rejects.toBeInstanceOf(APIError);
    try { await client.getValidationResult(operationID); }
    catch (error) { expect(String(error)).not.toContain("SECRET"); }
  });

  it("honors a bounded Retry-After before polling again", async () => {
    vi.useFakeTimers();
    try {
      let calls = 0;
      const transport: MachineClient = {
        async request() {
          calls++;
          if (calls === 1) return new Response(JSON.stringify({ id: operationID, status: "queued" }), {
            status: 200, headers: { "Content-Type": "application/json", "Retry-After": "2" },
          });
          return response(200, { id: operationID, status: "succeeded" });
        },
      };
      const pending = new EInvoiceClient("test", transport).waitValidation(operationID, 3000);
      await vi.advanceTimersByTimeAsync(1000);
      expect(calls).toBe(1);
      await vi.advanceTimersByTimeAsync(1000);
      expect((await pending).status).toBe("succeeded");
      expect(calls).toBe(2);
    } finally { vi.useRealTimers(); }
  });
});
