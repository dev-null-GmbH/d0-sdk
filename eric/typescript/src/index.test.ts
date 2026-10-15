import { createHash } from "node:crypto";
import { describe, expect, it } from "vitest";
import { APIError, EricClient, resourceFor, waitFor } from "./index.js";
import { operations } from "./operations.js";

const tenant = "11111111-1111-4111-8111-111111111111";
const product = "22222222-2222-4222-8222-222222222222";
const simulation = "33333333-3333-4333-8333-333333333333";
const key = "fixture-eric-001";
function machine(profile: "production" | "test") {
  const calls: Array<{ url: string; headers: Record<string,string>; method: string }> = [];
  const transport = { async request(url: string | URL, options?: { method?: string; headers?: Record<string,string>; body?: string }) {
    const target = String(url), path = new URL(target).pathname;
    calls.push({url:target, headers: options?.headers ?? {}, method: options?.method ?? "GET"});
    expect(target.startsWith(resourceFor(profile) + (profile === "production" ? "/v1" : "/v1"))).toBe(true);
    if (profile === "test") {
      expect(path.startsWith(`/eric/v1/tenants/${tenant}/products/${product}/simulations`)).toBe(true);
      const fixture = options?.body ? (JSON.parse(options.body) as {fixture:string}).fixture : "validation-accepted-v1";
      return new Response(JSON.stringify({id:simulation,fixture,status:"completed",outcome:fixture === "validation-accepted-v1" ? "simulated_accepted" : "simulated_rejected",simulated:true}), {status:options?.method === "POST" ? 202 : 200,headers:{"Content-Type":"application/json","X-Request-ID":"req-1"}});
    }
    if (path.endsWith("/notices")) return new Response(JSON.stringify({schema_version:"eric.user-notices.v1",version:"fixture",sdk_release:"fixture",documentation_archive_sha256:"0".repeat(64),license_document_sha256:"0".repeat(64),license_member:"license",notices:[]}),{status:200,headers:{"Content-Type":"application/json"}});
    if (path.endsWith("/payload.xml")) {
      const bytes = Buffer.from("<fixture/>");
      return new Response(bytes,{status:200,headers:{"Content-Type":"application/xml","Content-Digest":`sha-256=:${createHash("sha256").update(bytes).digest("base64")}:`}});
    }
    throw new Error(`unexpected fixture route ${path}`);
  }};
  return {client:new EricClient(profile,tenant,transport),calls};
}

describe("ERiC catalog and boundaries",()=>{
  it("binds every published operation and limits test to two simulations",async()=>{
    expect(Object.keys(operations)).toHaveLength(51);
    expect(Object.values(operations).filter(op=>op.profile === "production")).toHaveLength(49);
    expect(Object.values(operations).filter(op=>op.profile === "test")).toHaveLength(2);
    for (const op of Object.keys(operations)) expect(typeof (EricClient.prototype as unknown as Record<string,unknown>)[op]).toBe("function");
    const {client,calls}=machine("test");
    await expect(client.GetUserNotices({productId:product})).rejects.toThrow(/unavailable/);
    expect(calls).toHaveLength(0);
    for (const [fixture,outcome] of [["validation-accepted-v1","simulated_accepted"],["validation-rejected-v1","simulated_rejected"]] as const) {
      const result=await client.createEricTestSimulation({productId:product,idempotencyKey:key,body:{fixture}});
      expect(result.outcome).toBe(outcome);
      expect((await client.getEricTestSimulation({productId:product,simulationId:result.id})).simulated).toBe(true);
    }
    expect(calls.every(c=>c.headers["X-ERIC-Tenant"]===tenant)).toBe(true);
    expect(calls[0]?.url).toContain(`/tenants/${tenant}/`);
  });
  it("uses production base and rejects test methods there",async()=>{
    const {client,calls}=machine("production");
    expect((await client.GetUserNotices({productId:product})).schema_version).toBe("eric.user-notices.v1");
    await expect(client.createEricTestSimulation({productId:product,idempotencyKey:key,body:{fixture:"validation-accepted-v1"}})).rejects.toThrow(/unavailable/);
    expect(calls).toHaveLength(1);
  });
  it("verifies artifact bytes and rejects tampered digests",async()=>{
    const {client}=machine("production");
    const artifact=await client.GetPreparationArtifact({productId:product,preparationId:simulation,kind:"payload.xml"});
    expect(new TextDecoder().decode(artifact.bytes)).toBe("<fixture/>");
    const tampered=new EricClient("production",tenant,{request:async()=>new Response("<bad/>",{status:200,headers:{"Content-Type":"application/xml","Content-Digest":"sha-256=:invalid:"}})});
    await expect(tampered.GetPreparationArtifact({productId:product,preparationId:simulation,kind:"payload.xml"})).rejects.toThrow(/Digest/);
    const bytes=Buffer.from([0,1,255]);
    const digest=`sha-256=:${createHash("sha256").update(bytes).digest("base64")}:`;
    const lengthClient=new EricClient("production",tenant,{request:async()=>new Response(bytes,{status:200,headers:{"Content-Type":"application/octet-stream","Content-Digest":digest,"Content-Length":"4"}})});
    await expect(lengthClient.GetRetrievalArtifactContent({productId:product,artifactId:simulation,kind:"content",xEricActorStatus:"fixture-jws"})).rejects.toThrow(/Length/);
  });
  it("rejects invalid tenant and key before transport; safe problem metadata",async()=>{
    expect(()=>new EricClient("test","raw",{request:async()=>new Response()})).toThrow(/tenant/);
    const {client,calls}=machine("test");
    await expect(client.createEricTestSimulation({productId:product,idempotencyKey:"bad key",body:{fixture:"validation-accepted-v1"}})).rejects.toThrow(/idempotency/);
    await expect(client.getEricTestSimulation({productId:"raw",simulationId:simulation})).rejects.toThrow(/identifier/);
    expect(calls).toHaveLength(0);
    expect(new APIError(409).message).toBe("ERiC request failed (HTTP 409)");
    await expect(waitFor(async()=>1,()=>true,0)).rejects.toThrow(/timeout/);
  });
});
