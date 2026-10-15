"""Typed ERiC machine operations; OAuth and DPoP use d0-auth-machine."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import re
import threading
import time
import urllib.parse
from collections.abc import Callable, Mapping
from typing import Any, Literal

from d0_auth_machine import MachineClient
from joserfc.jwk import RSAKey

from .methods import EricOperations
from .operations import OPERATIONS

Profile = Literal["production", "test"]


def resource_for(profile: Profile) -> str:
    if profile == "production":
        return "https://api.d0.eu/eric"
    if profile == "test":
        return "https://api.test.d0.eu/eric"
    raise ValueError("unsupported ERiC profile")


class APIError(Exception):
    def __init__(self, status: int, problem_type: str = "", title: str = "", request_id: str = ""):
        super().__init__(f"ERiC request failed (HTTP {status})")
        self.status = status
        self.type = problem_type
        self.title = title
        self.request_id = request_id


_TENANT = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
_KEY = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
_SAFE_ID = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
_SAFE_HEADER = re.compile(r"^[!-~]{1,256}$")


class EricClient(EricOperations):
    def __init__(self, profile: Profile, tenant: str, transport: MachineClient):
        if not _TENANT.fullmatch(tenant):
            raise ValueError("invalid public tenant ID")
        if not isinstance(transport, MachineClient) or transport.resource != resource_for(profile):
            raise ValueError("shared machine client resource does not match ERiC profile")
        self.profile = profile
        self.tenant = tenant
        self.base = resource_for(profile) + ("/v1" if profile == "production" else "")
        self.transport = transport
        self.last_response: dict[str, str] = {"etag": "", "request_id": ""}

    @classmethod
    def create(cls, profile: Profile, tenant: str, client_id: str, key_id: str, signing_key: RSAKey, scopes: list[str]) -> EricClient:
        return cls(profile, tenant, MachineClient(client_id, key_id, signing_key, resource_for(profile), scopes))

    def _call(self, operation: str, request: Mapping[str, Any], cancel: threading.Event | None = None) -> Any:
        return self.call_with_response(operation, request, cancel)["data"]

    def call_with_response(self, operation: str, request: Mapping[str, Any], cancel: threading.Event | None = None) -> dict[str, Any]:
        """Return the result and its own ETag/request ID; safe for concurrent calls."""
        spec = OPERATIONS.get(operation)
        if spec is None:
            raise ValueError("unknown ERiC operation")
        if self.profile != spec["profile"]:
            raise ValueError("operation unavailable in selected ERiC environment")
        known = {p["name"] for p in spec["params"]}
        if request.keys() - known:
            raise ValueError("unknown ERiC request field")
        path = spec["path"]
        query: list[tuple[str, str]] = []
        headers = {"X-ERIC-Tenant": self.tenant}
        if spec["profile"] == "test":
            path = path.replace("{tenantId}", self.tenant)
        body: bytes | None = None
        for p in spec["params"]:
            value = request.get(p["name"])
            if value is None:
                if p["required"]:
                    raise ValueError(f"required {p['name']} missing")
                continue
            if p["in"] == "body":
                body = json.dumps(value, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
                continue
            if not isinstance(value, (str, int, bool)) or isinstance(value, float):
                raise TypeError(f"invalid {p['name']}")
            text = str(value).lower() if isinstance(value, bool) else str(value)
            if p["in"] == "path":
                if not _SAFE_ID.fullmatch(text) or (p.get("pattern") and not re.fullmatch(p["pattern"], text)) or (p.get("format") == "uuid" and not _TENANT.fullmatch(text)):
                    raise ValueError("invalid public identifier")
                path = path.replace("{" + p["wire"] + "}", urllib.parse.quote(text, safe=""))
            elif p["in"] == "query":
                query.append((p["wire"], text))
            elif p["in"] == "header":
                if not _SAFE_HEADER.fullmatch(text):
                    raise ValueError(f"invalid {p['name']}")
                headers[p["wire"]] = text
        if spec["method"] != "GET" and operation != "PlanEBilanzForm" and not _KEY.fullmatch(headers.get("Idempotency-Key", "")):
            raise ValueError("idempotency key must match ERiC contract")
        if body is not None:
            headers["Content-Type"] = spec["bodyType"]
        target = self.base + path
        if query:
            target += "?" + urllib.parse.urlencode(query)
        response = self.transport.request(target, method=spec["method"], headers=headers, body=body, cancel=cancel)
        try:
            maximum = 41_943_040
            raw: bytes = response.read(maximum + 1)
            if len(raw) > maximum:
                raise ValueError("ERiC response exceeds bound")
            request_id = response.headers.get("X-Request-ID", "")
            metadata = {"etag": response.headers.get("ETag", ""), "request_id": request_id if re.fullmatch(r"[!-~]{1,128}", request_id) else ""}
            self.last_response = metadata
            if response.status != spec["status"]:
                problem: dict[str, Any] = {}
                if response.headers.get("Content-Type", "").startswith("application/problem+json") and len(raw) <= 65_536:
                    try:
                        data = json.loads(raw)
                        if isinstance(data, dict):
                            problem = data
                    except ValueError:
                        pass
                ptype = problem.get("type", "")
                title = problem.get("title", "")
                raise APIError(response.status, ptype if isinstance(ptype, str) and len(ptype) <= 256 else "", title if isinstance(title, str) and len(title) <= 256 else "", metadata["request_id"])
            if spec["artifact"]:
                digest = response.headers.get("Content-Digest", "")
                actual = "sha-256=:" + base64.b64encode(hashlib.sha256(raw).digest()).decode("ascii") + ":"
                if not hmac.compare_digest(digest, actual):
                    raise ValueError("ERiC artifact Content-Digest mismatch")
                if spec["contentLength"] and response.headers.get("Content-Length") != str(len(raw)):
                    raise ValueError("ERiC artifact Content-Length mismatch")
                return {"data": {"bytes": raw, "contentType": response.headers.get("Content-Type", ""), "contentDigest": digest}, **metadata}
            if not response.headers.get("Content-Type", "").startswith("application/json"):
                raise ValueError("invalid ERiC response media type")
            return {"data": json.loads(raw), **metadata}
        finally:
            response.close()


__all__ = ["APIError", "EricClient", "Profile", "resource_for", "wait_for"]


def wait_for[T](fetch: Callable[[], T], terminal: Callable[[T], bool], timeout: float, cancel: threading.Event | None = None) -> T:
    """Poll a read operation for 1–120 seconds, cancellable between requests."""
    if not 1 <= timeout <= 120:
        raise ValueError("poll timeout must be 1s..2m")
    end = time.monotonic() + timeout
    signal = cancel or threading.Event()
    while not signal.is_set() and time.monotonic() < end:
        result = fetch()
        if terminal(result):
            return result
        signal.wait(min(1, max(0, end - time.monotonic())))
    raise TimeoutError("ERiC poll cancelled or timed out")
