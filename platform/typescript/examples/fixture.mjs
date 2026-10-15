import { PlatformClient, resourceFor } from "../dist/index.js";
for (const profile of ["production", "test"]) {
  const transport = { async request(url, options = {}) {
    if (!String(url).startsWith(resourceFor(profile) + "/v1/")) throw new Error("profile crossover");
    const path = new URL(url).pathname;
    if (path.endsWith("/domains") && (options.method ?? "GET") === "GET") return new Response(JSON.stringify({ domains: [{ fqdn: "example.eu", status: "active", created_at: "2026-01-01T00:00:00Z", updated_at: "2026-01-01T00:00:00Z" }] }), { status: 200, headers: { "Content-Type": "application/json" } });
    if (path.endsWith("/dns/records/www/A") && options.method === "PUT") return new Response(JSON.stringify({ name: "www.example.eu", type: "A", ttl: 300, records: ["192.0.2.1"], read_only: false }), { status: 200, headers: { "Content-Type": "application/json" } });
    throw new Error("unexpected route");
  } };
  const sdk = new PlatformClient(profile, transport);
  const domains = await sdk.listDomains({});
  const record = await sdk.upsertDNSRecord({ domain: domains.domains[0].fqdn, name: "www", type: "A", body: { records: ["192.0.2.1"], ttl: 300 } });
  if (record.name !== "www.example.eu") throw new Error("fixture failed");
  console.log(`${profile}: ${record.name}`);
}
