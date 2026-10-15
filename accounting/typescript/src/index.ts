/** Machine-only Accounting client. The named operation surface is catalog-generated. */
import { createMachineClient, type MachineClient, type MachineConfig } from "@dev-null-gmbh/auth-machine";
import { operations } from "./operations.js";
import type { OperationRequests, OperationResults } from "./generated.js";
export * from "./generated.js";

export type Profile = "production" | "test";
export function resourceFor(profile: Profile): string {
  if (profile === "production") return "https://api.d0.eu/accounting";
  if (profile === "test") return "https://api.test.d0.eu/accounting";
  throw new Error("Unsupported Accounting profile");
}
export type OperationName = keyof OperationRequests;
export type OperationMethods = { [K in OperationName]: (request: OperationRequests[K], signal?: AbortSignal) => Promise<OperationResults[K]> };
export type CallResult<T> = { data: T; etag: string; requestId: string };

/** A stable, bounded RFC 9457 problem; raw body and detail are discarded. */
export class APIError extends Error {
  constructor(public readonly status: number, public readonly type = "", public readonly title = "", public readonly requestId = "") {
    super(`Accounting request failed (HTTP ${status})`);
  }
}

const tenantID = /^ten_[0-9A-HJKMNP-TV-Z]{26}$/;
const idempotencyKey = /^[\x21-\x7e]{16,128}$/;
const safeID = /^[A-Za-z0-9_-]{1,128}$/;
const validOperation = (op: string): op is OperationName => Object.prototype.hasOwnProperty.call(operations, op);
function exactMoney(value: unknown): void {
  if (Array.isArray(value)) { for (const item of value) exactMoney(item); return; }
  if (!value || typeof value !== "object") return;
  const record = value as Record<string, unknown>;
  if ("amount" in record && "currency" in record && (typeof record.amount !== "string" || !/^-?(0|[1-9][0-9]{0,18})$/.test(record.amount)))
    throw new Error("Accounting amounts must be exact minor-unit decimal strings");
  for (const item of Object.values(record)) exactMoney(item);
}

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
      if (length > max) throw new Error("Accounting response exceeds bound");
      parts.push(value);
    }
  } catch (error) { await reader.cancel(); throw error; }
  finally { reader.releaseLock(); }
  return Buffer.concat(parts);
}

export class AccountingClient {
  readonly #base: string;
  readonly #profile: Profile;
  readonly #tenant: string;
  readonly #transport: MachineClient;
  constructor(profile: Profile, tenant: string, transport: MachineClient) {
    this.#base = resourceFor(profile) + "/v1";
    if (tenant !== "" && !tenantID.test(tenant)) throw new Error("Invalid public tenant ID");
    if (!transport || typeof transport.request !== "function") throw new Error("Shared machine transport required");
    this.#profile = profile;
    this.#tenant = tenant;
    this.#transport = transport;
  }
  static async create(profile: Profile, tenant: string, config: Omit<MachineConfig, "resource">): Promise<AccountingClient> {
    return new AccountingClient(profile, tenant, await createMachineClient({ ...config, resource: resourceFor(profile) }));
  }
  /** Convenience metadata; for concurrent calls use callWithResponse. */
  lastResponse: { etag: string; requestId: string } = { etag: "", requestId: "" };
  async call<K extends OperationName>(operation: K, request: OperationRequests[K], signal?: AbortSignal): Promise<OperationResults[K]> {
    return (await this.callWithResponse(operation, request, signal)).data;
  }
  /** Exact typed operation input/result plus its own ETag and request ID. */
  async callWithResponse<K extends OperationName>(operation: K, request: OperationRequests[K], signal?: AbortSignal): Promise<CallResult<OperationResults[K]>> {
    if (!validOperation(operation)) throw new Error("Unknown Accounting operation");
    const spec = operations[operation];
    if (this.#profile === "test" && !spec.test) throw new Error("Operation unavailable in Accounting test environment");
    if (!this.#tenant && operation !== "listTenants" && operation !== "createTenant") throw new Error("Selected public tenant ID required");
    const values = request as Record<string, unknown>;
    const known = new Set<string>(spec.params.map(p => p.name));
    for (const key of Object.keys(values)) if (!known.has(key)) throw new Error(`Unknown ${operation} request field`);
    let path: string = spec.path;
    const query = new URLSearchParams();
    const headers: Record<string, string> = {};
    if (this.#tenant) headers["X-Accounting-Tenant"] = this.#tenant;
    let body: string | undefined;
    for (const p of spec.params) {
      const value = values[p.name];
      if (value === undefined || value === null) {
        if (p.required) throw new Error(`Required ${p.name} missing`);
        continue;
      }
      if (p.in === "body") { exactMoney(value); body = JSON.stringify(value); continue; }
      if (typeof value !== "string" && typeof value !== "number" && typeof value !== "boolean") throw new Error(`Invalid ${p.name}`);
      const text = String(value);
      if (p.in === "path") {
        if (!safeID.test(text) || ("pattern" in p && p.pattern && !new RegExp(p.pattern).test(text))) throw new Error("Invalid public identifier");
        path = path.replace(`{${p.wire}}`, encodeURIComponent(text));
      } else if (p.in === "query") query.set(p.wire, text);
      else if (p.in === "header") {
        if (!/^[\x21-\x7e]{1,256}$/.test(text)) throw new Error(`Invalid ${p.name}`);
        headers[p.wire] = text;
      }
    }
    if (spec.method !== "GET" && !idempotencyKey.test(headers["Idempotency-Key"] ?? ""))
      throw new Error("Idempotency key must be 16–128 safe characters");
    if (body !== undefined) headers["Content-Type"] = spec.bodyType;
    const target = this.#base + path + (query.size ? `?${query}` : "");
    const response = await this.#transport.request(target, { method: spec.method, headers, body, signal });
    const binary = spec.responseType !== "application/json" && spec.responseType !== "";
    const raw = await bounded(response, binary ? 536_870_912 : 25_165_824);
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
    if (spec.status === 204) return { data: undefined as OperationResults[K], ...metadata };
    if (binary) {
      if (!(response.headers.get("Content-Type") ?? "").startsWith(spec.responseType)) throw new Error("Invalid Accounting response media type");
      return { data: raw as OperationResults[K], ...metadata };
    }
    if (!(response.headers.get("Content-Type") ?? "").startsWith("application/json")) throw new Error("Invalid Accounting response media type");
    try { return { data: JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(raw)) as OperationResults[K], ...metadata }; }
    catch { throw new Error("Invalid Accounting JSON response"); }
  }
}

// Operations are named and strictly typed through the generated interface below.
export interface AccountingClient extends OperationMethods {}
for (const operation of Object.keys(operations)) {
  Object.defineProperty(AccountingClient.prototype, operation, { value: function (this: AccountingClient, request: unknown, signal?: AbortSignal) {
    return this.call(operation as OperationName, request as OperationRequests[OperationName], signal);
  } });
}

/** Visit bounded pages without interpreting opaque public cursors. */
export async function walkPages<T>(fetch: (limit: number, after: string) => Promise<{ data: T[]; nextCursor?: string }>, visit: (items: T[]) => void | Promise<void>, limit = 100, maxPages = 100, after = ""): Promise<string> {
  if (!Number.isInteger(limit) || limit < 1 || limit > 100 || !Number.isInteger(maxPages) || maxPages < 1 || maxPages > 100) throw new Error("Pagination bounds must be 1..100");
  for (let i = 0; i < maxPages; i++) {
    const page = await fetch(limit, after);
    await visit(page.data);
    const next = page.nextCursor ?? "";
    if (!next) return "";
    if (next === after) throw new Error("Accounting cursor did not advance");
    after = next;
  }
  return after;
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
      if (controller.signal.aborted) throw new Error("Accounting poll cancelled or timed out");
      const value = await fetch(controller.signal);
      if (terminal(value)) return value;
      await new Promise<void>((resolve, reject) => {
        const onAbort = () => { clearTimeout(tick); reject(new Error("Accounting poll cancelled or timed out")); };
        const tick = setTimeout(() => { controller.signal.removeEventListener("abort", onAbort); resolve(); }, 1000);
        controller.signal.addEventListener("abort", onAbort, { once: true });
      });
    }
  } finally { clearTimeout(timer); signal?.removeEventListener("abort", cancel); }
}
