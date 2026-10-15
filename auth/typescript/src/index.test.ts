import { createHash } from "node:crypto";
import { generateKeyPair, importJWK, jwtVerify } from "jose";
import { afterEach, beforeAll, describe, expect, it, vi } from "vitest";
import { createMachineClient, type MachineConfig } from "./index.js";

let config: MachineConfig;
let publicKey: CryptoKey;
beforeAll(async () => {
  const keys = await generateKeyPair("PS256", { modulusLength: 3072 });
  publicKey = keys.publicKey;
  config = {
    clientId: "test-client",
    keyId: "test-key",
    signingKey: keys.privateKey,
    resource: "https://api.d0.eu/platform",
    scopes: ["platform.domains.read"],
  };
});
afterEach(() => vi.unstubAllGlobals());

function tokenResponse(overrides: Record<string, unknown> = {}) {
  return Response.json({
    access_token: "fixture-token",
    token_type: "DPoP",
    expires_in: 300,
    scope: "platform.domains.read",
    ...overrides,
  });
}

async function verifyProof(
  proof: string,
  url: string,
  method: string,
  nonce: string | undefined,
  token = "",
) {
  const verified = await jwtVerify(
    proof,
    async (header) => {
      expect(header.typ).toBe("dpop+jwt");
      expect(header.jwk).not.toHaveProperty("d");
      if (!header.jwk) throw new Error("missing proof JWK");
      return importJWK(header.jwk, "ES256");
    },
    { algorithms: ["ES256"], typ: "dpop+jwt" },
  );
  expect(verified.payload).toMatchObject({ htu: url, htm: method });
  expect(verified.payload.nonce).toBe(nonce);
  expect(verified.payload.ath).toBe(
    token ? createHash("sha256").update(token).digest("base64url") : undefined,
  );
  expect(Number.isInteger(verified.payload.iat)).toBe(true);
  return verified.payload.jti;
}

describe("machine transport", () => {
  it("cancels one caller without canceling shared refresh and snapshots mutable request bytes", async () => {
    const ready = Promise.withResolvers<void>();
    const issued = Promise.withResolvers<Response>();
    const network = vi.fn(async (url: URL, options: RequestInit) => {
      if (url.origin === "https://auth.d0.eu") {
        ready.resolve();
        return issued.promise;
      }
      expect(new TextDecoder().decode(options.body as Uint8Array)).toBe("original");
      expect(new Headers(options.headers).get("Idempotency-Key")).toBe("original-key");
      return new Response(null, { status: 204 });
    });
    vi.stubGlobal("fetch", network);
    const client = await createMachineClient(config);
    const controller = new AbortController();
    const canceled = client.request(`${config.resource}/v1/domains`, { signal: controller.signal });
    const rejection = expect(canceled).rejects.toMatchObject({ name: "AbortError" });
    await ready.promise;
    const bytes = new TextEncoder().encode("original");
    const headers = new Headers({ "Idempotency-Key": "original-key" });
    const operation = client.request(`${config.resource}/v1/domains`, {
      method: "POST",
      body: bytes,
      headers,
    });
    bytes.fill(0);
    headers.set("Idempotency-Key", "changed-key");
    controller.abort();
    await rejection;
    issued.resolve(tokenResponse());
    expect((await operation).status).toBe(204);
    expect(network).toHaveBeenCalledTimes(2);
  });

  it("does not retry invalid_client even when a nonce header is present", async () => {
    const network = vi.fn(async () =>
      Response.json(
        { error: "invalid_client", error_description: "private-response" },
        {
          status: 400,
          headers: { "DPoP-Nonce": "nonce" },
        },
      ),
    );
    vi.stubGlobal("fetch", network);
    const client = await createMachineClient(config);
    await expect(client.request(`${config.resource}/v1/domains`)).rejects.toThrow(
      "d0 token request rejected (HTTP 400)",
    );
    expect(network).toHaveBeenCalledTimes(1);
  });

  it("signs each attempt and preserves body, key and conditional headers across separate nonce challenges", async () => {
    const client = await createMachineClient(config);
    let tokens = 0;
    let requests = 0;
    const identifiers = new Set();
    vi.stubGlobal(
      "fetch",
      vi.fn(async (url: URL, options: RequestInit) => {
        expect(options.redirect).toBe("manual");
        expect(options.credentials).toBe("omit");
        const headers = new Headers(options.headers);
        if (url.origin === "https://auth.d0.eu") {
          const form = new URLSearchParams(options.body as string);
          const assertion = await jwtVerify(form.get("client_assertion") ?? "", publicKey, {
            algorithms: ["PS256"],
          });
          expect(assertion.protectedHeader).toMatchObject({ typ: "JWT", kid: config.keyId });
          expect(assertion.payload).toMatchObject({
            iss: config.clientId,
            sub: config.clientId,
            aud: "https://auth.d0.eu",
          });
          expect(Number(assertion.payload.exp) - Number(assertion.payload.iat)).toBe(60);
          expect(form.get("resource")).toBe(config.resource);
          expect(form.get("scope")).toBe(config.scopes[0]);
          identifiers.add(assertion.payload.jti);
          identifiers.add(
            await verifyProof(
              headers.get("DPoP") ?? "",
              url.href,
              "POST",
              tokens ? "as-nonce" : undefined,
            ),
          );
          if (tokens++ === 0)
            return Response.json(
              { error: "use_dpop_nonce" },
              { status: 400, headers: { "DPoP-Nonce": "as-nonce" } },
            );
          return tokenResponse();
        }
        expect(headers.get("Authorization")).toBe("DPoP fixture-token");
        expect(headers.get("Idempotency-Key")).toBe("stable-key");
        expect(headers.get("If-Match")).toBe('"version-1"');
        expect(new TextDecoder().decode(options.body as Uint8Array)).toBe('{"name":"unchanged"}');
        identifiers.add(
          await verifyProof(
            headers.get("DPoP") ?? "",
            `${config.resource}/v1/domains`,
            "POST",
            requests ? "api-nonce" : undefined,
            "fixture-token",
          ),
        );
        if (requests++ === 0)
          return new Response(null, {
            status: 401,
            headers: {
              "DPoP-Nonce": "api-nonce",
              "WWW-Authenticate": 'DPoP error="use_dpop_nonce"',
            },
          });
        return Response.json({ ok: true });
      }),
    );
    const response = await client.request(`${config.resource}/v1/domains?limit=1`, {
      method: "POST",
      body: '{"name":"unchanged"}',
      headers: { "Idempotency-Key": "stable-key", "If-Match": '"version-1"' },
    });
    expect(await response.json()).toEqual({ ok: true });
    expect([tokens, requests, identifiers.size]).toEqual([2, 2, 6]);
  });

  it("shares refresh but gives each concurrent operation a fresh proof", async () => {
    let tokens = 0;
    const proofs = new Set();
    vi.stubGlobal(
      "fetch",
      vi.fn(async (url: URL, options: RequestInit) => {
        if (url.origin === "https://auth.d0.eu") {
          tokens++;
          return tokenResponse();
        }
        proofs.add(
          await verifyProof(
            new Headers(options.headers).get("DPoP") ?? "",
            url.href,
            "GET",
            undefined,
            "fixture-token",
          ),
        );
        return new Response(null, { status: 204 });
      }),
    );
    const client = await createMachineClient(config);
    await Promise.all([1, 2, 3].map(() => client.request(`${config.resource}/v1/domains`)));
    expect([tokens, proofs.size]).toEqual([1, 3]);
  });

  it("signs test-resource requests and rejects its production counterpart", async () => {
    const testConfig = { ...config, resource: "https://api.test.d0.eu/platform" };
    const client = await createMachineClient(testConfig);
    await expect(
      createMachineClient({ ...testConfig, resource: "https://api.preview.d0.eu/platform" }),
    ).rejects.toThrow("resource");
    const network = vi.fn(async (url: URL, options: RequestInit) => {
      const proof = await verifyProof(
        new Headers(options.headers).get("DPoP") ?? "",
        url.origin + url.pathname,
        options.method ?? "GET",
        undefined,
        url.origin === "https://auth.d0.eu" ? "" : "fixture-token",
      );
      expect(proof).toBeTruthy();
      if (url.origin === "https://auth.d0.eu") {
        const form = new URLSearchParams(options.body as string);
        const assertion = await jwtVerify(form.get("client_assertion") ?? "", publicKey, {
          algorithms: ["PS256"],
        });
        expect(assertion.payload.aud).toBe("https://auth.d0.eu");
        expect(form.get("resource")).toBe(testConfig.resource);
        return tokenResponse();
      }
      expect(url.origin).toBe("https://api.test.d0.eu");
      return new Response(null, { status: 204 });
    });
    vi.stubGlobal("fetch", network);
    expect((await client.request(`${testConfig.resource}/v1/domains`)).status).toBe(204);
    await expect(client.request("https://api.d0.eu/platform/v1/domains")).rejects.toThrow(
      "canonical resource",
    );
    expect(network).toHaveBeenCalledTimes(2);
  });

  it.each(["POST", "PUT", "PATCH", "DELETE"])(
    "leaves %s key requirements to the product contract",
    async (method) => {
      const network = vi.fn(async (url: URL, options: RequestInit) => {
        if (url.origin === "https://auth.d0.eu") return tokenResponse();
        expect(new Headers(options.headers).has("Idempotency-Key")).toBe(false);
        expect(new TextDecoder().decode(options.body as Uint8Array)).toBe("{}");
        return new Response(null, { status: 204 });
      });
      vi.stubGlobal("fetch", network);
      const client = await createMachineClient(config);
      expect(
        (await client.request(`${config.resource}/v1/contract-operation`, { method, body: "{}" }))
          .status,
      ).toBe(204);
      for (const key of ["", "contains space", "x".repeat(129)]) {
        await expect(
          client.request(`${config.resource}/v1/contract-operation`, {
            method,
            body: "{}",
            headers: { "Idempotency-Key": key },
          }),
        ).rejects.toThrow("Idempotency-Key");
      }
      expect(network).toHaveBeenCalledTimes(2);
    },
  );

  it.each([
    ["https://foreign.invalid/platform/v1/domains", {}],
    ["https://api.d0.eu/accounting/v1/documents", {}],
    ["https://api.test.d0.eu/platform/v1/domains", {}],
    ["https://api.d0.eu/platform/v1/domains#fragment", {}],
    ["https://api.d0.eu/platform/v1/%2e%2e/other", {}],
    ["https://api.d0.eu/platform/v1/domains?access_token=secret", {}],
    ["https://api.d0.eu/platform/v1/domains", { headers: { Authorization: "Bearer secret" } }],
    ["https://api.d0.eu/platform/v1/domains", { headers: { Host: "foreign.invalid" } }],
    [
      "https://api.d0.eu/platform/v1/domains",
      { method: "POST", body: "{}", headers: { "Idempotency-Key": "" } },
    ],
  ])("rejects untrusted target or request before network", async (url, options) => {
    const network = vi.fn();
    vi.stubGlobal("fetch", network);
    const client = await createMachineClient(config);
    await expect(client.request(url, options)).rejects.toThrow();
    expect(network).not.toHaveBeenCalled();
  });

  it.each([
    { token_type: "Bearer" },
    { expires_in: 301 },
    { expires_in: 0 },
    { scope: "platform.domains.write" },
    { scope: "platform.domains.read platform.domains.read" },
  ])("rejects invalid token profile", async (invalid) => {
    const network = vi.fn(async () => tokenResponse(invalid));
    vi.stubGlobal("fetch", network);
    const client = await createMachineClient(config);
    await expect(client.request(`${config.resource}/v1/domains`)).rejects.toThrow("token response");
    expect(network).toHaveBeenCalledTimes(1);
  });

  it.each([307, 429, 401])(
    "never follows redirects or retries business status %i",
    async (status) => {
      const network = vi.fn(async (url: URL) =>
        url.origin === "https://auth.d0.eu"
          ? tokenResponse()
          : new Response(null, {
              status,
              headers: { Location: "https://foreign.invalid", "Retry-After": "10" },
            }),
      );
      vi.stubGlobal("fetch", network);
      const client = await createMachineClient(config);
      if (status === 307)
        await expect(client.request(`${config.resource}/v1/domains`)).rejects.toThrow("redirects");
      else expect((await client.request(`${config.resource}/v1/domains`)).status).toBe(status);
      expect(network).toHaveBeenCalledTimes(2);
    },
  );

  it("bounds nonce loops and token bodies", async () => {
    const network = vi.fn(async () =>
      Response.json(
        { error: "use_dpop_nonce" },
        {
          status: 400,
          headers: { "DPoP-Nonce": "nonce" },
        },
      ),
    );
    vi.stubGlobal("fetch", network);
    let client = await createMachineClient(config);
    await expect(client.request(`${config.resource}/v1/domains`)).rejects.toThrow();
    expect(network).toHaveBeenCalledTimes(2);
    network.mockImplementation(async () => new Response("x".repeat(32769)));
    client = await createMachineClient(config);
    await expect(client.request(`${config.resource}/v1/domains`)).rejects.toThrow("size");
    expect(network).toHaveBeenCalledTimes(3);
  });
});
