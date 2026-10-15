import { describe, expect, it } from "vitest";
import { APIError, PlatformClient, resourceFor, walkAuditEvents, waitFor, type Profile } from "./index.js";
import { operations } from "./operations.js";

function fixture(profile: Profile) {
  const calls: Array<{ url: string; method: string }> = [];
  const transport = { async request(url: string | URL, options?: { method?: string }) {
    const target = String(url);
    expect(target.startsWith(resourceFor(profile) + "/v1/")).toBe(true);
    const path = new URL(target).pathname;
    calls.push({ url: target, method: options?.method ?? "GET" });
    let status = 200;
    let payload: unknown;
    if (path.endsWith("/domains") && options?.method === "GET") payload = { domains: [{ fqdn: "example.eu", status: "active", created_at: "2026-01-01T00:00:00Z", updated_at: "2026-01-01T00:00:00Z" }] };
    else if (path.endsWith("/dns/records/www/A") && options?.method === "PUT") payload = { name: "www.example.eu", type: "A", ttl: 300, records: ["192.0.2.1"], read_only: false };
    else if (path.endsWith("/dns/records") && options?.method === "GET") payload = { records: [{ name: "www.example.eu", type: "A", ttl: 300, records: ["192.0.2.1"], read_only: false }] };
    else if (path.endsWith("/dns/records/www/A") && options?.method === "DELETE") { status = 204; payload = undefined; }
    else throw new Error("unexpected fixture route");
    return new Response(payload === undefined ? null : JSON.stringify(payload), { status, headers: { "Content-Type": "application/json", ETag: '"fixture-v1"', "X-Request-ID": "fixture-request" } });
  } };
  return { client: new PlatformClient(profile, transport), calls };
}

describe("Platform machine contract", () => {
  it("covers exactly 30 production and 5 test operations", () => {
    expect(Object.keys(operations)).toHaveLength(30);
    expect(Object.values(operations).filter(op => op.test)).toHaveLength(5);
    for (const op of Object.keys(operations)) expect(typeof (PlatformClient.prototype as unknown as Record<string, unknown>)[op]).toBe("function");
  });
  for (const profile of ["production", "test"] as const) it(`runs ${profile} DNS fixture with fixed host`, async () => {
    const { client, calls } = fixture(profile);
    const domains = await client.listDomains({});
    expect(domains.domains?.[0]?.fqdn).toBe("example.eu");
    const record = await client.upsertDNSRecord({ domain: "example.eu", name: "www", type: "A", body: { records: ["192.0.2.1"], ttl: 300 } });
    expect(record.name).toBe("www.example.eu");
    const listing = await client.callWithResponse("listDNSRecords", { domain: "example.eu" });
    expect(listing.requestId).toBe("fixture-request");
    expect(listing.etag).toBe('"fixture-v1"');
    expect(listing.data.records?.[0]?.records?.[0]).toBe("192.0.2.1");
    await client.deleteDNSRecord({ domain: "example.eu", name: "www", type: "A" });
    expect(calls).toHaveLength(4);
    if (profile === "test") {
      await expect(client.getClusterCatalog({})).rejects.toThrow(/unavailable/);
      expect(calls).toHaveLength(4);
    }
  });
  it("rejects path escapes and unsafe numeric prices before egress", async () => {
    const { client, calls } = fixture("production");
    await expect(client.getDomain({ domain: "../secret" })).rejects.toThrow(/identifier/);
    await expect(client.quoteCluster({ body: { vcpu: Number.MAX_SAFE_INTEGER + 1, memory_gib: 2, storage_gib: 10 } })).rejects.toThrow(/exact range/);
    expect(calls).toHaveLength(0);
  });
  it("exposes bounded problem metadata only", async () => {
    const sdk = new PlatformClient("test", { async request() { return new Response(JSON.stringify({ type: "conflict", title: "Conflict", detail: "secret" }), { status: 409, headers: { "Content-Type": "application/problem+json", "X-Request-ID": "req-1" } }); } });
    await expect(sdk.listDomains({})).rejects.toMatchObject({ status: 409, type: "conflict", title: "Conflict", requestId: "req-1" });
    expect(new APIError(409).message).not.toContain("secret");
  });
  it("retains all int64 minor-unit price digits", async () => {
    const sdk = new PlatformClient("production", { async request() {
      return new Response('{"price":{"amount_cents":9007199254740993,"currency":"EUR","interval":"monthly"},"spec":{"vcpu":1,"memory_gib":2,"storage_gib":10,"public_ipv4":false}}', { status: 200, headers: { "Content-Type": "application/json" } });
    } });
    const quote = await sdk.quoteCluster({ body: { vcpu: 1, memory_gib: 2, storage_gib: 10 } });
    expect(quote.price.amount_cents).toBe("9007199254740993");
  });
  it("requires caller-owned idempotency keys and handles an empty 202", async () => {
    let calls = 0;
    const sdk = new PlatformClient("production", { async request() { calls++; return new Response(null, { status: 202 }); } });
    await expect(sdk.deleteCluster({ id: "cl_fixture", idempotencyKey: "short" })).rejects.toThrow(/Idempotency/);
    expect(calls).toBe(0);
    await expect(sdk.deleteObjectStorageBucket({ id: "bucket_fixture" })).resolves.toBeUndefined();
    expect(calls).toBe(1);
    await expect(sdk.call("deleteCluster", { id: "cl_fixture" } as never)).rejects.toThrow(/missing/);
    expect(calls).toBe(1);
  });
  it("walks audit keysets and respects cancellation", async () => {
    const cursors: string[] = [];
    const sdk = new PlatformClient("production", { async request(url) {
      const before = new URL(String(url)).searchParams.get("before") ?? "";
      cursors.push(before);
      return new Response(JSON.stringify({ events: [], next_before: before ? "" : "older" }), { status: 200, headers: { "Content-Type": "application/json" } });
    } });
    let pages = 0;
    expect(await walkAuditEvents(sdk, () => { pages++; }, 2, 3)).toBe("");
    expect(cursors).toEqual(["", "older"]);
    expect(pages).toBe(2);
    const abort = new AbortController(); abort.abort();
    await expect(waitFor(async () => 0, value => value === 1, 1000, abort.signal)).rejects.toThrow();
  });
});
