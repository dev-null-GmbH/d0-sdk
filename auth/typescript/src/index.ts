import { createHash, randomUUID } from "node:crypto";
import { exportJWK, generateKeyPair, type JWK, SignJWT } from "jose";

const issuer = "https://auth.d0.eu";
const tokenEndpoint = new URL(`${issuer}/oauth2/token`);
const resources = ["https://api.d0.eu", "https://api.test.d0.eu"].flatMap((origin) =>
  ["platform", "accounting", "einvoice", "eric"].map((name) => `${origin}/${name}`),
);

export interface MachineConfig {
  clientId: string;
  keyId: string;
  resource: string;
  scopes: readonly string[];
  /** A locally imported RSA-PSS/SHA-256 private CryptoKey, at least 3072 bits. */
  signingKey: CryptoKey;
}

export interface MachineRequest {
  method?: string;
  headers?: HeadersInit;
  /** Buffered bytes are copied before authentication so a nonce retry is identical. */
  body?: string | Uint8Array;
  signal?: AbortSignal;
}

export interface MachineClient {
  /** Requests are restricted to this client's resource/v1 namespace. */
  request(url: string | URL, options?: MachineRequest): Promise<Response>;
}

function safe(value: unknown, maximum: number): value is string {
  return (
    typeof value === "string" &&
    value.length > 0 &&
    value.length <= maximum &&
    /^[\x21-\x7e]+$/.test(value)
  );
}

/** Creates a Node.js client with independent assertion and in-memory proof keys. */
export async function createMachineClient(config: MachineConfig): Promise<MachineClient> {
  if (
    !resources.includes(config.resource) ||
    !safe(config.clientId, 128) ||
    !safe(config.keyId, 128)
  ) {
    throw new Error("Invalid d0 resource, client ID or key ID");
  }
  const key = config.signingKey;
  const algorithm = key?.algorithm as RsaHashedKeyAlgorithm | undefined;
  if (
    !(key instanceof CryptoKey) ||
    key.type !== "private" ||
    !key.usages.includes("sign") ||
    algorithm?.name !== "RSA-PSS" ||
    algorithm.hash.name !== "SHA-256" ||
    algorithm.modulusLength < 3072
  ) {
    throw new Error("An RSA-PSS SHA-256 signing key of at least 3072 bits is required");
  }
  const scopes = [...config.scopes].sort();
  const prefix = `${config.resource.split("/").at(-1)}.`;
  if (
    !scopes.length ||
    scopes.length > 64 ||
    new Set(scopes).size !== scopes.length ||
    scopes.some((scope) => !safe(scope, 128) || !scope.startsWith(prefix))
  ) {
    throw new Error("Invalid, duplicate or foreign resource scope");
  }
  const proof = await generateKeyPair("ES256");
  return new Client({ ...config, scopes }, proof.privateKey, await exportJWK(proof.publicKey));
}

class Client implements MachineClient {
  #config: MachineConfig;
  #proofKey: CryptoKey;
  #proofPublic: JWK;
  #token = "";
  #expires = 0;
  #refresh: Promise<string> | undefined;
  #authorizationNonce: string | undefined;
  #resourceNonce: string | undefined;

  constructor(config: MachineConfig, proofKey: CryptoKey, proofPublic: JWK) {
    this.#config = config;
    this.#proofKey = proofKey;
    this.#proofPublic = proofPublic;
  }

  async request(target: string | URL, options: MachineRequest = {}): Promise<Response> {
    let url: URL;
    try {
      url = new URL(target);
    } catch {
      throw new Error("Invalid API URL");
    }
    const prefix = `${new URL(this.#config.resource).pathname}/v1`;
    if (
      url.origin !== new URL(this.#config.resource).origin ||
      url.username ||
      url.password ||
      url.hash ||
      (url.pathname !== prefix && !url.pathname.startsWith(`${prefix}/`)) ||
      url.pathname.includes("//") ||
      url.pathname.includes("/.") ||
      /%2f|%5c|%2e/i.test(url.pathname)
    ) {
      throw new Error("Request is outside the configured canonical resource");
    }
    for (const name of url.searchParams.keys()) {
      if (
        ["access_token", "authorization", "dpop", "client_assertion"].includes(name.toLowerCase())
      ) {
        throw new Error("Credentials are forbidden in request queries");
      }
    }
    const method = (options.method ?? "GET").toUpperCase();
    const headers = new Headers(options.headers);
    for (const name of [
      "Authorization",
      "DPoP",
      "Host",
      "Cookie",
      "Proxy-Authorization",
      "Content-Length",
      "Transfer-Encoding",
    ]) {
      if (headers.has(name))
        throw new Error("Caller-provided credentials or transport overrides are forbidden");
    }
    if (!["GET", "HEAD", "POST", "PUT", "PATCH", "DELETE"].includes(method))
      throw new Error("Unsupported API method");
    if (headers.has("Idempotency-Key") && !safe(headers.get("Idempotency-Key"), 128))
      throw new Error("Invalid Idempotency-Key");
    if ((method === "GET" || method === "HEAD") && options.body !== undefined)
      throw new Error("Read requests cannot carry a body");
    if (
      options.body !== undefined &&
      typeof options.body !== "string" &&
      !(options.body instanceof Uint8Array)
    ) {
      throw new Error("Request body must be replayable bytes or a string");
    }
    const body =
      options.body === undefined
        ? undefined
        : typeof options.body === "string"
          ? new TextEncoder().encode(options.body)
          : new Uint8Array(options.body);
    const signal = AbortSignal.any([
      AbortSignal.timeout(45000),
      ...(options.signal ? [options.signal] : []),
    ]);
    signal.throwIfAborted();
    const token = await untilAborted(this.#accessToken(), signal);
    for (let attempt = 0; attempt < 2; attempt++) {
      headers.set("Authorization", `DPoP ${token}`);
      headers.set("DPoP", await this.#signProof(method, url, this.#resourceNonce, token));
      const response = await send(url, { method, headers, ...(body ? { body } : {}), signal });
      const nonce = responseNonce(response.headers);
      if (nonce) this.#resourceNonce = nonce;
      if (response.status >= 300 && response.status < 400 && response.status !== 304) {
        await response.body?.cancel();
        throw new Error("Authenticated API redirects are forbidden");
      }
      if (
        attempt === 0 &&
        response.status === 401 &&
        nonce &&
        /^DPoP .*\berror="use_dpop_nonce"/.test(response.headers.get("WWW-Authenticate") ?? "")
      ) {
        await response.body?.cancel();
        continue;
      }
      return response;
    }
    throw new Error("DPoP nonce retry exhausted");
  }

  #accessToken(): Promise<string> {
    if (this.#expires - Date.now() > 30000) return Promise.resolve(this.#token);
    if (!this.#refresh) {
      this.#refresh = this.#fetchToken().finally(() => {
        this.#refresh = undefined;
      });
    }
    return this.#refresh;
  }

  async #fetchToken(): Promise<string> {
    const signal = AbortSignal.timeout(10000);
    for (let attempt = 0; attempt < 2; attempt++) {
      const now = Math.floor(Date.now() / 1000);
      const assertion = await new SignJWT({
        iss: this.#config.clientId,
        sub: this.#config.clientId,
        aud: issuer,
        iat: now,
        exp: now + 60,
        jti: randomUUID(),
      })
        .setProtectedHeader({ alg: "PS256", typ: "JWT", kid: this.#config.keyId })
        .sign(this.#config.signingKey);
      const body = new URLSearchParams({
        grant_type: "client_credentials",
        client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        client_assertion: assertion,
        resource: this.#config.resource,
        scope: this.#config.scopes.join(" "),
      }).toString();
      const proof = await this.#signProof("POST", tokenEndpoint, this.#authorizationNonce);
      const response = await send(tokenEndpoint, {
        method: "POST",
        body,
        signal,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          Accept: "application/json",
          DPoP: proof,
        },
      });
      const result = await tokenJSON(response);
      const nonce = responseNonce(response.headers);
      if (nonce) this.#authorizationNonce = nonce;
      if (response.status !== 200) {
        if (attempt === 0 && response.status === 400 && nonce && result.error === "use_dpop_nonce")
          continue;
        throw new Error(`d0 token request rejected (HTTP ${response.status})`);
      }
      if (
        !safe(result.access_token, 16384) ||
        result.token_type !== "DPoP" ||
        typeof result.expires_in !== "number" ||
        !Number.isInteger(result.expires_in) ||
        result.expires_in < 1 ||
        result.expires_in > 300 ||
        typeof result.scope !== "string" ||
        result.scope.split(" ").sort().join(" ") !== this.#config.scopes.join(" ")
      ) {
        throw new Error("Invalid DPoP token response");
      }
      this.#token = result.access_token;
      this.#expires = (now + result.expires_in) * 1000;
      return this.#token;
    }
    throw new Error("Authorization nonce retry exhausted");
  }

  #signProof(method: string, url: URL, nonce?: string, token?: string): Promise<string> {
    return new SignJWT({
      htm: method,
      htu: url.origin + url.pathname,
      iat: Math.floor(Date.now() / 1000),
      jti: randomUUID(),
      ...(nonce ? { nonce } : {}),
      ...(token ? { ath: createHash("sha256").update(token).digest("base64url") } : {}),
    })
      .setProtectedHeader({ alg: "ES256", typ: "dpop+jwt", jwk: this.#proofPublic })
      .sign(this.#proofKey);
  }
}

function responseNonce(headers: Headers): string | undefined {
  const value = headers.get("DPoP-Nonce");
  return safe(value, 512) && !value.includes(",") ? value : undefined;
}

async function send(url: URL, options: RequestInit): Promise<Response> {
  try {
    return await fetch(url, {
      ...options,
      redirect: "manual",
      credentials: "omit",
      cache: "no-store",
      referrerPolicy: "no-referrer",
    });
  } catch {
    if (options.signal?.aborted) throw new DOMException("d0 request aborted", "AbortError");
    throw new Error(
      "d0 transport failed; preserve the original operation and idempotency key after an uncertain outcome",
    );
  }
}

async function tokenJSON(response: Response): Promise<Record<string, unknown>> {
  const reader = response.body?.getReader();
  if (!reader) throw new Error("Invalid token response");
  let size = 0;
  const chunks: Uint8Array[] = [];
  try {
    while (true) {
      const part = await reader.read();
      if (part.done) break;
      size += part.value.length;
      if (size > 32768) throw new Error("Invalid token response size");
      chunks.push(part.value);
    }
    const parsed: unknown = JSON.parse(Buffer.concat(chunks).toString("utf8"));
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed))
      throw new Error("Invalid token response");
    return parsed as Record<string, unknown>;
  } catch {
    await reader.cancel().catch(() => undefined);
    throw new Error(size > 32768 ? "Invalid token response size" : "Invalid token response");
  } finally {
    reader.releaseLock();
  }
}

function untilAborted<T>(pending: Promise<T>, signal: AbortSignal): Promise<T> {
  return new Promise((resolve, reject) => {
    const aborted = () => reject(new DOMException("d0 request aborted", "AbortError"));
    signal.addEventListener("abort", aborted, { once: true });
    pending.then(resolve, reject).finally(() => signal.removeEventListener("abort", aborted));
    if (signal.aborted) aborted();
  });
}
