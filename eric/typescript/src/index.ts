/** Machine-only ERiC client. The named operation surface is catalog-generated. */
import { createHash } from "node:crypto";
import { createMachineClient, type MachineClient, type MachineConfig } from "@dev-null-gmbh/auth-machine";
import { operations } from "./operations.js";
import type { OperationRequests, OperationResults } from "./generated.js";
export * from "./generated.js";

export type Environment = "production" | "test";
export function resourceFor(profile: Environment): string {
  if (profile === "production") return "https://api.d0.eu/eric";
  if (profile === "test") return "https://api.test.d0.eu/eric";
  throw new Error("Unsupported ERiC profile");
}
export type OperationName = keyof OperationRequests;
export type OperationMethods = { [K in OperationName]: (request: OperationRequests[K], signal?: AbortSignal) => Promise<OperationResults[K]> };
export type CallResult<T> = { data: T; etag: string; requestId: string };

/** A stable, bounded RFC 9457 problem; raw body and detail are discarded. */
export class APIError extends Error {
  constructor(public readonly status: number, public readonly type = "", public readonly title = "", public readonly requestId = "") {
    super(`ERiC request failed (HTTP ${status})`);
  }
}

const tenantID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
const idempotencyKey = /^[A-Za-z0-9._:-]{1,128}$/;
const safeID = /^[A-Za-z0-9._:-]{1,128}$/;
const validOperation = (op: string): op is OperationName => Object.prototype.hasOwnProperty.call(operations, op);
async function bounded(response: Response, max: number): Promise<Uint8Array> {
  const reader = response.body?.getReader();
  if (!reader) return new Uint8Array();
  const parts: Uint8Array[] = [];
  let length = 0;
  try {
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      length += value.byteLength;
      if (length > max) throw new Error("ERiC response exceeds bound");
      parts.push(value);
    }
  } catch (error) { await reader.cancel(); throw error; }
  finally { reader.releaseLock(); }
  return Buffer.concat(parts);
}

export class EricClient {
  readonly #base: string;
  readonly #profile: Environment;
  readonly #tenant: string;
  readonly #transport: MachineClient;
  constructor(profile: Environment, tenant: string, transport: MachineClient) {
    this.#base = resourceFor(profile) + (profile === "production" ? "/v1" : "");
    if (!tenantID.test(tenant)) throw new Error("Invalid public tenant ID");
    if (!transport || typeof transport.request !== "function") throw new Error("Shared machine transport required");
    this.#profile = profile;
    this.#tenant = tenant;
    this.#transport = transport;
  }
  static async create(profile: Environment, tenant: string, config: Omit<MachineConfig, "resource">): Promise<EricClient> {
    return new EricClient(profile, tenant, await createMachineClient({ ...config, resource: resourceFor(profile) }));
  }
  /** Convenience metadata; for concurrent calls use callWithResponse. */
  lastResponse: { etag: string; requestId: string } = { etag: "", requestId: "" };
  async call<K extends OperationName>(operation: K, request: OperationRequests[K], signal?: AbortSignal): Promise<OperationResults[K]> {
    return (await this.callWithResponse(operation, request, signal)).data;
  }
  /** Exact typed operation input/result plus its own ETag and request ID. */
  async callWithResponse<K extends OperationName>(operation: K, request: OperationRequests[K], signal?: AbortSignal): Promise<CallResult<OperationResults[K]>> {
    if (!validOperation(operation)) throw new Error("Unknown ERiC operation");
    const spec = operations[operation];
    if (this.#profile !== spec.profile) throw new Error("Operation unavailable in selected ERiC environment");
    const values = request as Record<string, unknown>;
    const known = new Set<string>(spec.params.map(p => p.name));
    for (const key of Object.keys(values)) if (!known.has(key)) throw new Error(`Unknown ${operation} request field`);
    let path: string = spec.path;
    const headers: Record<string, string> = {};
    headers["X-ERIC-Tenant"] = this.#tenant;
    if (spec.profile === "test") path = path.replace("{tenantId}", encodeURIComponent(this.#tenant));
    let body: string | undefined;
    for (const p of spec.params) {
      const value = values[p.name];
      if (value === undefined || value === null) {
        if (p.required) throw new Error(`Required ${p.name} missing`);
        continue;
      }
      if (p.in === "body") { body = JSON.stringify(value); continue; }
      if (typeof value !== "string" && typeof value !== "number" && typeof value !== "boolean") throw new Error(`Invalid ${p.name}`);
      const text = String(value);
      if (p.in === "path") {
        if (!safeID.test(text) || ("pattern" in p && p.pattern && !new RegExp(p.pattern).test(text)) || ("format" in p && p.format === "uuid" && !tenantID.test(text))) throw new Error("Invalid public identifier");
        path = path.replace(`{${p.wire}}`, encodeURIComponent(text));
      } else if (p.in === "header") {
        if (!/^[\x21-\x7e]{1,256}$/.test(text)) throw new Error(`Invalid ${p.name}`);
        headers[p.wire] = text;
      }
    }
    if (spec.method !== "GET" && operation !== "PlanEBilanzForm" && !idempotencyKey.test(headers["Idempotency-Key"] ?? ""))
      throw new Error("Idempotency key must match ERiC contract");
    if (body !== undefined) headers["Content-Type"] = spec.bodyType;
    const target = this.#base + path;
    const response = await this.#transport.request(target, { method: spec.method, headers, body, signal });
    const raw = await bounded(response, 41_943_040);
    const requestId = response.headers.get("X-Request-ID") ?? "";
    const metadata = { etag: response.headers.get("ETag") ?? "", requestId: /^[\x21-\x7e]{1,128}$/.test(requestId) ? requestId : "" };
    this.lastResponse = metadata;
    if (response.status !== spec.status) {
      let problem: Record<string, unknown> = {};
      if ((response.headers.get("Content-Type") ?? "").startsWith("application/problem+json") && raw.length <= 65_536) {
        try { const parsed = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(raw)) as unknown; if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) problem = parsed as Record<string, unknown>; } catch { /* opaque */ }
      }
      const type = typeof problem.type === "string" && problem.type.length <= 256 ? problem.type : "";
      const title = typeof problem.title === "string" && problem.title.length <= 256 ? problem.title : "";
      throw new APIError(response.status, type, title, metadata.requestId);
    }
    if (spec.artifact) {
      const digest = response.headers.get("Content-Digest") ?? "";
      const actual = `sha-256=:${createHash("sha256").update(raw).digest("base64")}:`;
      if (digest !== actual) throw new Error("ERiC artifact Content-Digest mismatch");
      if (spec.contentLength && response.headers.get("Content-Length") !== String(raw.length)) throw new Error("ERiC artifact Content-Length mismatch");
      return { data: { bytes: raw, contentType: response.headers.get("Content-Type") ?? "", contentDigest: digest } as OperationResults[K], ...metadata };
    }
    if (!(response.headers.get("Content-Type") ?? "").startsWith("application/json")) throw new Error("Invalid ERiC response media type");
    try { return { data: JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(raw)) as OperationResults[K], ...metadata }; }
    catch { throw new Error("Invalid ERiC JSON response"); }
  }
}

// Operations are named and strictly typed through the generated interface below.
export interface EricClient extends OperationMethods {}
for (const operation of Object.keys(operations)) {
  Object.defineProperty(EricClient.prototype, operation, { value: function (this: EricClient, request: unknown, signal?: AbortSignal) {
    return this.call(operation as OperationName, request as OperationRequests[OperationName], signal);
  } });
}

/** Poll an asynchronous read operation for a caller-selected bound of at most two minutes. */
export async function waitFor<T>(fetch: (signal: AbortSignal) => Promise<T>, terminal: (value: T) => boolean, timeoutMs: number, signal?: AbortSignal): Promise<T> {
  if (!Number.isInteger(timeoutMs) || timeoutMs < 1000 || timeoutMs > 120_000) throw new Error("Poll timeout must be 1s..2m");
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  const cancel = () => controller.abort();
  signal?.addEventListener("abort", cancel, { once: true });
  try {
    for (;;) {
      if (controller.signal.aborted) throw new Error("ERiC poll cancelled or timed out");
      const value = await fetch(controller.signal);
      if (terminal(value)) return value;
      await new Promise<void>((resolve, reject) => {
        const onAbort = () => { clearTimeout(tick); reject(new Error("ERiC poll cancelled or timed out")); };
        const tick = setTimeout(() => { controller.signal.removeEventListener("abort", onAbort); resolve(); }, 1000);
        controller.signal.addEventListener("abort", onAbort, { once: true });
      });
    }
  } finally { clearTimeout(timer); signal?.removeEventListener("abort", cancel); }
}
