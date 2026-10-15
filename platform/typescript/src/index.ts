/** Machine-only Platform client. The named operation surface is contract-generated. */
import { createMachineClient, type MachineClient, type MachineConfig } from "@dev-null-gmbh/auth-machine";
import { operations } from "./operations.js";
import type { OperationRequests, OperationResults } from "./generated.js";
export * from "./generated.js";

export type Profile = "production" | "test";
export function resourceFor(profile: Profile): string {
  if (profile === "production") return "https://api.d0.eu/platform";
  if (profile === "test") return "https://api.test.d0.eu/platform";
  throw new Error("Unsupported Platform profile");
}
export type OperationName = keyof OperationRequests;
export type OperationMethods = { [K in OperationName]: (request: OperationRequests[K], signal?: AbortSignal) => Promise<OperationResults[K]> };
export type CallResult<T> = { data: T; etag: string; requestId: string };

/** A stable, bounded RFC 9457 problem; raw body and detail are discarded. */
export class APIError extends Error {
  constructor(public readonly status: number, public readonly type = "", public readonly title = "", public readonly requestId = "") {
    super(`Platform request failed (HTTP ${status})`);
  }
}

const idempotencyKey = /^[\x21-\x7e]{16,128}$/;
const safeID = /^[A-Za-z0-9_.@*-]{1,253}$/;
const validOperation = (op: string): op is OperationName => Object.prototype.hasOwnProperty.call(operations, op);
function safeNumbers(value: unknown): void {
  if (typeof value === "number" && (!Number.isFinite(value) || (Number.isInteger(value) && !Number.isSafeInteger(value))))
    throw new Error("Platform integer exceeds JavaScript exact range");
  if (Array.isArray(value)) for (const item of value) safeNumbers(item);
  else if (value && typeof value === "object") for (const item of Object.values(value)) safeNumbers(item);
}
function parseExactJSON(raw: Uint8Array): unknown {
  const source = new TextDecoder("utf-8", { fatal: true }).decode(raw);
  // Prices are int64 cents on the wire. Quote just those JSON number tokens
  // before JSON.parse can round them, and expose their exact decimal strings.
  let cursor = 0;
  let converted = "";
  for (let i = 0; i < source.length; i++) {
    if (source[i] !== '"') continue;
    let end = i + 1;
    while (end < source.length) {
      if (source[end] === "\\") { end += 2; continue; }
      if (source[end] === '"') break;
      end++;
    }
    if (end >= source.length) break;
    const token = source.slice(i, end + 1);
    const key = JSON.parse(token) as string;
    let colon = end + 1;
    while (/\s/.test(source[colon] ?? "")) colon++;
    if (source[colon] === ":" && /^[A-Za-z0-9_]*_cents$/.test(key)) {
      let start = colon + 1;
      while (/\s/.test(source[start] ?? "")) start++;
      const number = /^-?(?:0|[1-9]\d*)/.exec(source.slice(start))?.[0];
      if (!number || !/[,}\]\s]/.test(source[start + number.length] ?? "")) throw new Error("Invalid Platform cents value");
      const cents = BigInt(number);
      if (cents < -(1n << 63n) || cents >= (1n << 63n)) throw new Error("Platform cents exceed int64 range");
      converted += source.slice(cursor, start) + JSON.stringify(number);
      cursor = start + number.length;
      i = cursor - 1;
    } else i = end;
  }
  converted += source.slice(cursor);
  const bare = converted.replace(/"(?:\\.|[^"\\])*"/g, '""');
  for (const match of bare.matchAll(/-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/g)) {
    const token = match[0];
    if (!/[.eE]/.test(token) && (BigInt(token) > BigInt(Number.MAX_SAFE_INTEGER) || BigInt(token) < -BigInt(Number.MAX_SAFE_INTEGER)))
      throw new Error("Platform integer exceeds JavaScript exact range");
  }
  return JSON.parse(converted) as unknown;
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
      if (length > max) throw new Error("Platform response exceeds bound");
      parts.push(value);
    }
  } catch (error) { await reader.cancel(); throw error; }
  finally { reader.releaseLock(); }
  return Buffer.concat(parts);
}

export class PlatformClient {
  readonly #base: string;
  readonly #profile: Profile;
  readonly #transport: MachineClient;
  constructor(profile: Profile, transport: MachineClient) {
    this.#base = resourceFor(profile) + "/v1";
    if (!transport || typeof transport.request !== "function") throw new Error("Shared machine transport required");
    this.#profile = profile;
    this.#transport = transport;
  }
  static async create(profile: Profile, config: Omit<MachineConfig, "resource">): Promise<PlatformClient> {
    return new PlatformClient(profile, await createMachineClient({ ...config, resource: resourceFor(profile) }));
  }
  /** Convenience metadata; for concurrent calls use callWithResponse. */

  async call<K extends OperationName>(operation: K, request: OperationRequests[K], signal?: AbortSignal): Promise<OperationResults[K]> {
    return (await this.callWithResponse(operation, request, signal)).data;
  }
  /** Exact typed operation input/result plus its own ETag and request ID. */
  async callWithResponse<K extends OperationName>(operation: K, request: OperationRequests[K], signal?: AbortSignal): Promise<CallResult<OperationResults[K]>> {
    if (!validOperation(operation)) throw new Error("Unknown Platform operation");
    const spec = operations[operation];
    if (this.#profile === "test" && !spec.test) throw new Error("Operation unavailable in Platform test environment");
    const values = request as Record<string, unknown>;
    const known = new Set<string>(spec.params.map(p => p.name));
    for (const key of Object.keys(values)) if (!known.has(key)) throw new Error(`Unknown ${operation} request field`);
    let path: string = spec.path;
    const query = new URLSearchParams();
    const headers: Record<string, string> = {};
    let body: string | undefined;
    for (const p of spec.params) {
      const value = values[p.name];
      if (value === undefined || value === null) {
        if (p.required) throw new Error(`Required ${p.name} missing`);
        continue;
      }
      if (p.in === "body") { safeNumbers(value); body = JSON.stringify(value); continue; }
      if (typeof value !== "string" && typeof value !== "number" && typeof value !== "boolean") throw new Error(`Invalid ${p.name}`);
      if (typeof value === "number" && (!Number.isSafeInteger(value) || ("minimum" in p && value < p.minimum) || ("maximum" in p && value > p.maximum))) throw new Error(`Invalid ${p.name}`);
      if (typeof value === "string" && (("minLength" in p && value.length < p.minLength) || ("maxLength" in p && value.length > p.maxLength))) throw new Error(`Invalid ${p.name}`);
      if ("enum" in p && !(p.enum as readonly unknown[]).includes(value)) throw new Error(`Invalid ${p.name}`);
      const text = String(value);
      if (p.in === "path") {
        if (!safeID.test(text) || text === "." || text === ".." || ("pattern" in p && p.pattern && !new RegExp(p.pattern).test(text))) throw new Error("Invalid public identifier");
        path = path.replace(`{${p.wire}}`, encodeURIComponent(text));
      } else if (p.in === "query") query.set(p.wire, text);
      else if (p.in === "header") {
        if (!/^[\x21-\x7e]{1,256}$/.test(text)) throw new Error(`Invalid ${p.name}`);
        headers[p.wire] = text;
      }
    }
    if (headers["Idempotency-Key"] !== undefined && !idempotencyKey.test(headers["Idempotency-Key"]))
      throw new Error("Idempotency key must be 16–128 safe characters");
    if (body !== undefined) headers["Content-Type"] = spec.bodyType;
    const target = this.#base + path + (query.size ? `?${query}` : "");
    const response = await this.#transport.request(target, { method: spec.method, headers, body, signal });
    const raw = await bounded(response, 25_165_824);
    const requestId = response.headers.get("X-Request-ID") ?? "";
    const metadata = { etag: response.headers.get("ETag") ?? "", requestId: /^[\x21-\x7e]{1,128}$/.test(requestId) ? requestId : "" };
    if (!(spec.statuses as readonly number[]).includes(response.status)) {
      let problem: Record<string, unknown> = {};
      if ((response.headers.get("Content-Type") ?? "").startsWith("application/problem+json") && raw.length <= 65_536) {
        try { const parsed = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(raw)) as unknown; if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) problem = parsed as Record<string, unknown>; } catch { /* opaque */ }
      }
      const type = typeof problem.type === "string" && problem.type.length <= 256 ? problem.type : "";
      const title = typeof problem.title === "string" && problem.title.length <= 256 ? problem.title : "";
      throw new APIError(response.status, type, title, metadata.requestId);
    }
    if ((spec.emptyStatuses as readonly number[]).includes(response.status)) return { data: undefined as OperationResults[K], ...metadata };
    if (!(response.headers.get("Content-Type") ?? "").startsWith("application/json")) throw new Error("Invalid Platform response media type");
    try { return { data: parseExactJSON(raw) as OperationResults[K], ...metadata }; }
    catch { throw new Error("Invalid Platform JSON response"); }
  }
}

// Operations are named and strictly typed through the generated interface below.
export interface PlatformClient extends OperationMethods {}
for (const operation of Object.keys(operations)) {
  Object.defineProperty(PlatformClient.prototype, operation, { value: function (this: PlatformClient, request: unknown, signal?: AbortSignal) {
    return this.call(operation as OperationName, request as OperationRequests[OperationName], signal);
  } });
}

/** Traverse Platform audit keysets without interpreting opaque cursors. */
export async function walkAuditEvents(client: PlatformClient, visit: (events: OperationResults["listAuditEvents"]["events"]) => void | Promise<void>, limit = 100, maxPages = 100, before = "", signal?: AbortSignal): Promise<string> {
  if (!Number.isInteger(limit) || limit < 1 || limit > 500 || !Number.isInteger(maxPages) || maxPages < 1 || maxPages > 100) throw new Error("Audit pagination bounds invalid");
  for (let i = 0; i < maxPages; i++) {
    signal?.throwIfAborted();
    const page = await client.listAuditEvents(before ? { limit, before } : { limit }, signal);
    await visit(page.events);
    if (!page.next_before) return "";
    if (page.next_before === before) throw new Error("Platform audit cursor did not advance");
    before = page.next_before;
  }
  return before;
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
      if (controller.signal.aborted) throw new Error("Platform poll cancelled or timed out");
      const value = await fetch(controller.signal);
      if (terminal(value)) return value;
      await new Promise<void>((resolve, reject) => {
        const onAbort = () => { clearTimeout(tick); reject(new Error("Platform poll cancelled or timed out")); };
        const tick = setTimeout(() => { controller.signal.removeEventListener("abort", onAbort); resolve(); }, 1000);
        controller.signal.addEventListener("abort", onAbort, { once: true });
      });
    }
  } finally { clearTimeout(timer); signal?.removeEventListener("abort", cancel); }
}
