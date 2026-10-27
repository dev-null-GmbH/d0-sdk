import { describe, expect, it } from "vitest";
import { AccountingClient, APIError, resourceFor } from "./index.js";
import { operations } from "./operations.js";

const suffix = "9GXQ8W5V4R3P2N1M0KJHGF7ED6";
const tenant = "ten_" + suffix;
const account = "acct_" + suffix;
const period = "per_" + suffix;
const entry = "je_" + suffix;
const key = "fixture-key-00000001";

function fixture(profile: "production" | "test") {
  const calls: Array<{ url: string; method: string; headers: Record<string, string>; body?: string }> = [];
  const transport = { async request(url: string | URL, options?: { method?: string; headers?: Record<string, string>; body?: string }) {
    const target = String(url);
    expect(target.startsWith(resourceFor(profile) + "/v1/")).toBe(true);
    const path = new URL(target).pathname;
    calls.push({ url: target, method: options?.method ?? "GET", headers: options?.headers ?? {}, body: options?.body });
    let status = 200;
    let payload: object = {};
    if (path.endsWith("/accounts") && options?.method === "POST") { status = 201; payload = { id: account, accountNo: JSON.parse(options.body ?? "{}").accountNo, name: "Bank", createdAt: "2026-01-01T00:00:00Z" }; }
    else if (path.endsWith("/periods") && options?.method === "POST") { status = 201; payload = { id: period, label: "2026-01", startsOn: "2026-01-01", endsOn: "2026-01-31", status: "open", createdAt: "2026-01-01T00:00:00Z" }; }
    else if (path.endsWith("/journal-entries") && options?.method === "POST") {
      status = 201;
      const body = JSON.parse(options.body ?? "{}") as { lines: Array<{ amount: { amount: string }; side: string }> };
      expect(body.lines.map(line => line.amount.amount)).toEqual(["150000", "150000"]);
      expect(body.lines.map(line => line.side)).toEqual(["debit", "credit"]);
      payload = { id: entry, periodId: period, status: "draft", bookingDate: "2026-01-15", currency: "EUR", lines: body.lines, createdAt: "2026-01-01T00:00:00Z" };
    } else throw new Error("unexpected fixture route: " + path);
    return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json", ETag: '"fixture-v1"', "X-Request-ID": "fixture-request" } });
  } };
  return { client: new AccountingClient(profile, tenant, transport), calls };
}

describe("pinned operation surface", () => {
  it("has all 80 production and exactly 12 test operations", () => {
    expect(Object.keys(operations)).toHaveLength(80);
    expect(Object.values(operations).filter(op => op.test)).toHaveLength(12);
    for (const op of Object.keys(operations)) expect(typeof (AccountingClient.prototype as unknown as Record<string, unknown>)[op]).toBe("function");
  });
  for (const profile of ["production", "test"] as const) it(`runs a balanced ${profile} draft without posting`, async () => {
    const { client, calls } = fixture(profile);
    const debit = await client.createAccount({ idempotencyKey: key, body: { accountNo: "1200", name: "Bank" } });
    const credit = await client.createAccount({ idempotencyKey: "fixture-key-00000002", body: { accountNo: "4000", name: "Revenue" } });
    const p = await client.createPeriod({ idempotencyKey: "fixture-key-00000003", body: { label: "2026-01", startsOn: "2026-01-01", endsOn: "2026-01-31" } });
    const draft = await client.createJournalEntryDraft({ idempotencyKey: "fixture-key-00000004", body: { periodId: p.id, bookingDate: "2026-01-15", currency: "EUR", lines: [
      { accountId: debit.id, side: "debit", amount: { amount: "150000", currency: "EUR" } },
      { accountId: credit.id, side: "credit", amount: { amount: "150000", currency: "EUR" } },
    ] } });
    expect(draft.status).toBe("draft");
    expect(client.lastResponse.etag).toBe('"fixture-v1"');
    const conditional = await client.callWithResponse("createAccount", { idempotencyKey: "fixture-key-00000006", body: { accountNo: "1000", name: "Cash" } });
    expect(conditional.etag).toBe('"fixture-v1"');
    expect(conditional.requestId).toBe("fixture-request");
    expect(calls).toHaveLength(5);
    for (const call of calls) { expect(call.headers["X-Accounting-Tenant"]).toBe(tenant); expect(call.headers["Idempotency-Key"]?.length).toBeGreaterThanOrEqual(16); }
    if (profile === "test") {
      await expect(client.postJournalEntry({ entryId: entry, idempotencyKey: "fixture-key-00000005" })).rejects.toThrow(/unavailable/);
      expect(calls).toHaveLength(5);
    }
  });
  it("rejects missing preconditions and unsafe tenant IDs before transport", async () => {
    expect(() => new AccountingClient("test", "tenant-raw", { request: async () => new Response() })).toThrow();
    const { client, calls } = fixture("test");
    await expect(client.createAccount({ idempotencyKey: "short", body: { accountNo: "1200", name: "Bank" } })).rejects.toThrow(/Idempotency/);
    await expect(client.createJournalEntryDraft({ idempotencyKey: key, body: { periodId: period, bookingDate: "2026-01-15", currency: "EUR", lines: [
      { accountId: account, side: "debit", amount: { amount: 150000 as unknown as string, currency: "EUR" } },
      { accountId: account, side: "credit", amount: { amount: "150000", currency: "EUR" } },
    ] } })).rejects.toThrow(/decimal strings/);
    expect(calls).toHaveLength(0);
  });
  it("exposes only bounded problem metadata", () => {
    const error = new APIError(409, "conflict", "Conflict", "req-1");
    expect(error.status).toBe(409);
    expect(error.message).not.toContain("raw");
  });
  it("blocks all 24 banking operations in the isolated test profile", async () => {
    const { client, calls } = fixture("test");
    const banking = Object.entries(operations).filter(([, op]) => op.path.startsWith("/bank"));
    expect(banking).toHaveLength(24);
    for (const [operation] of banking) {
      await expect(client.call(operation as keyof typeof operations, {} as never)).rejects.toThrow(/unavailable/);
    }
    expect(calls).toHaveLength(0);
  });
  it("rejects numeric bank amounts before transport", async () => {
    const { client, calls } = fixture("production");
    await expect(client.createBankAllocation({ movementId: "btxn_" + suffix, idempotencyKey: key, body: {
      expectedRevision: 1, expectedReviewRevision: 1, entryId: entry, lineNo: 1, amountCents: 1000 as unknown as string,
    } })).rejects.toThrow(/decimal strings/);
    expect(calls).toHaveLength(0);
  });
});
