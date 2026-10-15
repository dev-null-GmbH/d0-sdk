import { AccountingClient, resourceFor } from "../dist/index.js";

const suffix = "9GXQ8W5V4R3P2N1M0KJHGF7ED6";
for (const profile of ["production", "test"]) {
  const transport = { async request(target, options) {
    if (!String(target).startsWith(resourceFor(profile) + "/v1/")) throw new Error("profile crossover");
    const path = new URL(target).pathname;
    const input = JSON.parse(options.body);
    let response;
    if (path.endsWith("/accounts")) response = { id: "acct_" + suffix, accountNo: input.accountNo, name: input.name, createdAt: "2026-01-01T00:00:00Z" };
    else if (path.endsWith("/periods")) response = { id: "per_" + suffix, ...input, status: "open", createdAt: "2026-01-01T00:00:00Z" };
    else if (path.endsWith("/journal-entries")) {
      if (input.lines.length !== 2 || input.lines[0].amount.amount !== input.lines[1].amount.amount || input.lines[0].side !== "debit" || input.lines[1].side !== "credit") throw new Error("unbalanced fixture");
      response = { id: "je_" + suffix, status: "draft", ...input, createdAt: "2026-01-01T00:00:00Z" };
    } else throw new Error("unexpected fixture operation");
    return new Response(JSON.stringify(response), { status: 201, headers: { "Content-Type": "application/json" } });
  } };
  const sdk = new AccountingClient(profile, "ten_" + suffix, transport);
  const debit = await sdk.createAccount({ idempotencyKey: "fixture-account-00001", body: { accountNo: "1200", name: "Bank" } });
  const credit = await sdk.createAccount({ idempotencyKey: "fixture-account-00002", body: { accountNo: "4000", name: "Revenue" } });
  const period = await sdk.createPeriod({ idempotencyKey: "fixture-period-00001", body: { label: "2026-01", startsOn: "2026-01-01", endsOn: "2026-01-31" } });
  const draft = await sdk.createJournalEntryDraft({ idempotencyKey: "fixture-draft-000001", body: { periodId: period.id, bookingDate: "2026-01-15", currency: "EUR", lines: [
    { accountId: debit.id, side: "debit", amount: { amount: "150000", currency: "EUR" } },
    { accountId: credit.id, side: "credit", amount: { amount: "150000", currency: "EUR" } },
  ] } });
  process.stdout.write(`${profile}: balanced unposted draft ${draft.id}\n`);
}
