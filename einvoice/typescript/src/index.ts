import { createHash } from "node:crypto";
import {
  createMachineClient,
  type MachineClient,
  type MachineConfig,
} from "@dev-null-gmbh/auth-machine";

export type Profile = "production" | "test";
export function resourceFor(profile: Profile): string {
  if (profile === "production") return "https://api.d0.eu/einvoice";
  if (profile === "test") return "https://api.test.d0.eu/einvoice";
  throw new Error("Unsupported EInvoice profile");
}

export interface ByteIdentity { sizeBytes: number; sha256: string; contentDigest: string }
export interface Document {
  schema: "d0.einvoice.document.v1"; id: string; mediaType: "application/xml";
  byteIdentity: ByteIdentity; createdAt: string; expiresAt: string;
}
export type ValidationStatus = "queued" | "running" | "succeeded" | "failed";
export interface ValidationOperation {
  schema: "d0.einvoice.validation-operation.v1"; id: string;
  documentId: string; validationPolicyId: string; status: ValidationStatus;
  requestedAt: string; updatedAt: string; startedAt?: string; completedAt?: string;
  resultId?: string; resultUri?: string;
  failure?: { code: "source-unavailable" | "processor-unavailable" | "validation-processing-failed" };
}
export interface EvidenceComponent {
  kind: "processor" | "validator" | "ruleset"; name: string; version: string;
  artifactSha256: string; artifactContentDigest: string;
}
export interface ValidationPolicy {
  schema: "d0.einvoice.validation-policy.v1"; id: string; name: string; description?: string;
  version: string; status: "available" | "deprecated" | "withdrawn";
  manifestSha256: string; manifestContentDigest: string;
  acceptedSyntaxes: ("ubl" | "cii")[]; profiles: string[];
  validator: EvidenceComponent; rulesets: EvidenceComponent[]; publishedAt: string;
}
export interface PolicyPage {
  schema: "d0.einvoice.validation-policy-page.v1"; items: ValidationPolicy[]; nextCursor?: string;
}
export interface ValidationIssue {
  severity: "error" | "warning" | "information"; code: string; message: string; location?: string;
}
export interface ValidationResult {
  schema: "d0.einvoice.validation-result.v1"; id: string; operationId: string;
  source: { documentId: string; mediaType: "application/xml"; byteIdentity: ByteIdentity };
  validationPolicy: { id: string; version: string; manifestSha256: string; manifestContentDigest: string };
  valid: boolean; syntax: "ubl" | "cii" | "unknown"; profile?: string;
  validatedAt: string;
  evidence: { processor: EvidenceComponent; validator: EvidenceComponent; rulesets: EvidenceComponent[] };
  issues: ValidationIssue[];
}

/** Bounded structural error. Invoice bytes and server problem details stay out. */
export class APIError extends Error {
  constructor(
    public readonly status: number,
    public readonly type = "",
    public readonly title = "",
    public readonly requestId = "",
  ) { super(`EInvoice request failed (HTTP ${status})`); }
}

const idPattern = /^(?:doc_|vop_|vpol_)[A-Za-z0-9]{20,80}$/;
const keyPattern = /^[A-Za-z0-9._~:+/=-]{16,128}$/;
function checkId(id: string, prefix: string): void {
  if (typeof id !== "string" || !id.startsWith(prefix) || !idPattern.test(id))
    throw new Error("Invalid EInvoice identifier");
}
function checkKey(key: string): void {
  if (typeof key !== "string" || !keyPattern.test(key))
    throw new Error("Idempotency key must be 16–128 contract-safe characters");
}
async function boundedJSON(response: Response): Promise<unknown> {
  const reader = response.body?.getReader();
  if (!reader) throw new Error("Invalid EInvoice response");
  const parts: Uint8Array[] = [];
  let size = 0;
  try {
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > 25_165_824) throw new Error("Oversized EInvoice response");
      parts.push(value);
    }
  } catch (error) {
    await reader.cancel();
    throw error;
  } finally { reader.releaseLock(); }
  if (size === 0) return null;
  try { return JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(Buffer.concat(parts))); }
  catch { throw new Error("Invalid EInvoice response"); }
}

export class EInvoiceClient {
  readonly #base: string;
  readonly #transport: MachineClient;
  constructor(profile: Profile, transport: MachineClient) {
    this.#base = resourceFor(profile) + "/v1";
    if (!transport || typeof transport.request !== "function") throw new Error("Machine transport required");
    this.#transport = transport;
  }
  async #call<T>(
    path: string, expected: number, options: {
      method?: "GET" | "POST"; key?: string; media?: string;
      body?: Uint8Array; digest?: string; signal?: AbortSignal;
      retry?: (delayMs: number) => void;
    } = {},
  ): Promise<T> {
    const headers = new Headers({ Accept: "application/json" });
    if (options.key) headers.set("Idempotency-Key", options.key);
    if (options.media) headers.set("Content-Type", options.media);
    if (options.digest) headers.set("Content-Digest", options.digest);
    const response = await this.#transport.request(this.#base + path, {
      method: options.method ?? "GET", headers,
      ...(options.body ? { body: options.body } : {}), signal: options.signal,
    });
    let data: unknown;
    try { data = await boundedJSON(response); }
    catch (error) {
      if (response.status !== expected) throw new APIError(response.status);
      throw error;
    }
    if (response.status !== expected) {
      const problem = data && typeof data === "object" ? data as Record<string, unknown> : {};
      const coherent = problem.status === response.status;
      const type = coherent && typeof problem.type === "string" && problem.type.length <= 2048 &&
        problem.type.startsWith("https://api.d0.eu/einvoice/problems/") ? problem.type : "";
      const title = coherent && typeof problem.title === "string" && problem.title.length <= 256 ? problem.title : "";
      const header = response.headers.get("X-Request-ID") ?? "";
      const requestId = /^[\x21-\x7e]{1,128}$/.test(header) ? header : "";
      throw new APIError(response.status, type, title, requestId);
    }
    if (!(response.headers.get("Content-Type") ?? "").startsWith("application/json") ||
        data === null || typeof data !== "object" || Array.isArray(data))
      throw new Error("Invalid EInvoice response");
    if (options.retry) {
      const raw = response.headers.get("Retry-After") ?? "";
      const seconds = Number(raw);
      options.retry(Number.isInteger(seconds) && seconds >= 1 && seconds <= 300 && String(seconds) === raw ? seconds * 1000 : 1000);
    }
    return data as T;
  }
  createDocument(xml: Uint8Array, idempotencyKey: string, signal?: AbortSignal): Promise<Document> {
    checkKey(idempotencyKey);
    if (!(xml instanceof Uint8Array) || xml.byteLength < 1 || xml.byteLength > 20_971_520)
      throw new Error("Invalid XML byte length");
    const body = new Uint8Array(xml);
    const digest = `sha-256=:${createHash("sha256").update(body).digest("base64")}:`;
    return this.#call("/documents", 201, { method: "POST", key: idempotencyKey, media: "application/xml", body, digest, signal });
  }
  getDocument(id: string, signal?: AbortSignal): Promise<Document> {
    checkId(id, "doc_"); return this.#call("/documents/" + id, 200, { signal });
  }
  createValidationOperation(documentId: string, policyId: string, idempotencyKey: string, signal?: AbortSignal): Promise<ValidationOperation> {
    checkId(documentId, "doc_"); checkId(policyId, "vpol_"); checkKey(idempotencyKey);
    const body = new TextEncoder().encode(JSON.stringify({ documentId, validationPolicyId: policyId }));
    return this.#call("/validation-operations", 202, { method: "POST", key: idempotencyKey, media: "application/json", body, signal });
  }
  getValidationOperation(id: string, signal?: AbortSignal): Promise<ValidationOperation> {
    return this.#readValidationOperation(id, signal);
  }
  #readValidationOperation(id: string, signal?: AbortSignal, retry?: (delayMs: number) => void): Promise<ValidationOperation> {
    checkId(id, "vop_"); return this.#call("/validation-operations/" + id, 200, { signal, retry });
  }
  getValidationResult(id: string, signal?: AbortSignal): Promise<ValidationResult> {
    checkId(id, "vop_"); return this.#call("/validation-operations/" + id + "/result", 200, { signal });
  }
  listValidationPolicies(limit = 50, cursor = "", signal?: AbortSignal): Promise<PolicyPage> {
    if (!Number.isInteger(limit) || limit < 1 || limit > 100 || typeof cursor !== "string" || cursor.length > 1024)
      throw new Error("Invalid policy page");
    const query = new URLSearchParams({ limit: String(limit) });
    if (cursor) query.set("cursor", cursor);
    return this.#call("/validation-policies?" + query.toString(), 200, { signal });
  }
  getValidationPolicy(id: string, signal?: AbortSignal): Promise<ValidationPolicy> {
    checkId(id, "vpol_"); return this.#call("/validation-policies/" + id, 200, { signal });
  }
  async waitValidation(id: string, maxWaitMs: number, signal?: AbortSignal): Promise<ValidationOperation> {
    checkId(id, "vop_");
    if (!Number.isInteger(maxWaitMs) || maxWaitMs < 1 || maxWaitMs > 120_000)
      throw new Error("Polling limit must be within two minutes");
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(new Error("Validation poll timed out")), maxWaitMs);
    const combined = AbortSignal.any([controller.signal, ...(signal ? [signal] : [])]);
    try {
      for (;;) {
        combined.throwIfAborted();
        let delayMs = 1000;
        const operation = await this.#readValidationOperation(id, combined, value => { delayMs = value; });
        if (operation.status === "succeeded" || operation.status === "failed") return operation;
        if (operation.status !== "queued" && operation.status !== "running") throw new Error("Invalid validation state");
        await new Promise<void>((resolve, reject) => {
          const timer = setTimeout(() => { combined.removeEventListener("abort", aborted); resolve(); }, delayMs);
          const aborted = () => { clearTimeout(timer); reject(combined.reason); };
          combined.addEventListener("abort", aborted, { once: true });
          if (combined.aborted) aborted();
        });
      }
    } finally { clearTimeout(timeout); }
  }
}

export async function createEInvoiceClient(profile: Profile, config: Omit<MachineConfig, "resource">): Promise<EInvoiceClient> {
  const transport = await createMachineClient({ ...config, resource: resourceFor(profile) });
  return new EInvoiceClient(profile, transport);
}
