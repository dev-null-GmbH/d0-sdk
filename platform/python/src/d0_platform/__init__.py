"""Typed Platform machine operations; OAuth and DPoP use d0-auth-machine."""
from __future__ import annotations

import json
import math
import re
import threading
import urllib.parse
from collections.abc import Callable, Mapping
from typing import Any, Literal

from d0_auth_machine import MachineClient
from joserfc.jwk import RSAKey

from .methods import PlatformOperations
from .operations import OPERATIONS

Profile = Literal["production", "test"]


def resource_for(profile: Profile) -> str:
    if profile == "production":
        return "https://api.d0.eu/platform"
    if profile == "test":
        return "https://api.test.d0.eu/platform"
    raise ValueError("unsupported Platform profile")


class APIError(Exception):
    def __init__(self, status: int, problem_type: str = "", title: str = "", request_id: str = ""):
        super().__init__(f"Platform request failed (HTTP {status})")
        self.status = status
        self.type = problem_type
        self.title = title
        self.request_id = request_id


_KEY = re.compile(r"^[!-~]{16,128}$")
_SAFE_ID = re.compile(r"^[A-Za-z0-9_.@*-]{1,253}$")
_SAFE_HEADER = re.compile(r"^[!-~]{1,256}$")


def _bounded_numbers(value: Any) -> None:
    if isinstance(value, list):
        for item in value:
            _bounded_numbers(item)
    elif isinstance(value, dict):
        for item in value.values():
            _bounded_numbers(item)
    elif isinstance(value, int) and not isinstance(value, bool) and not -(2**63) <= value < 2**63:
        raise ValueError("Platform integer exceeds int64 range")
    elif isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Platform number is not finite")


class PlatformClient(PlatformOperations):
    def __init__(self, profile: Profile, transport: MachineClient):
        if not isinstance(transport, MachineClient) or transport.resource != resource_for(profile):
            raise ValueError("shared machine client resource does not match Platform profile")
        self.profile = profile
        self.base = resource_for(profile) + "/v1"
        self.transport = transport

    @classmethod
    def create(cls, profile: Profile, client_id: str, key_id: str, signing_key: RSAKey, scopes: list[str]) -> PlatformClient:
        return cls(profile, MachineClient(client_id, key_id, signing_key, resource_for(profile), scopes))

    def _call(self, operation: str, request: Mapping[str, Any], cancel: threading.Event | None = None) -> Any:
        return self.call_with_response(operation, request, cancel)["data"]

    def call_with_response(self, operation: str, request: Mapping[str, Any], cancel: threading.Event | None = None) -> dict[str, Any]:
        """Return the result and its own ETag/request ID; safe for concurrent calls."""
        spec = OPERATIONS.get(operation)
        if spec is None:
            raise ValueError("unknown Platform operation")
        if self.profile == "test" and not spec["test"]:
            raise ValueError("operation unavailable in Platform test environment")
        known = {p["name"] for p in spec["params"]}
        if request.keys() - known:
            raise ValueError("unknown Platform request field")
        path = spec["path"]
        query: list[tuple[str, str]] = []
        headers: dict[str, str] = {}
        body: bytes | None = None
        for p in spec["params"]:
            value = request.get(p["name"])
            if value is None:
                if p["required"]:
                    raise ValueError(f"required {p['name']} missing")
                continue
            if p["in"] == "body":
                _bounded_numbers(value)
                body = json.dumps(value, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
                continue
            if not isinstance(value, (str, int, bool)) or isinstance(value, float):
                raise TypeError(f"invalid {p['name']}")
            if isinstance(value, int) and not isinstance(value, bool) and (
                not -(2**63) <= value < 2**63 or value < p.get("minimum", value) or value > p.get("maximum", value)
            ):
                raise ValueError(f"invalid {p['name']}")
            if isinstance(value, str) and (len(value) < p.get("minLength", 0) or len(value) > p.get("maxLength", 1024)):
                raise ValueError(f"invalid {p['name']}")
            if "enum" in p and value not in p["enum"]:
                raise ValueError(f"invalid {p['name']}")
            text = str(value).lower() if isinstance(value, bool) else str(value)
            if p["in"] == "path":
                if not _SAFE_ID.fullmatch(text) or text in (".", "..") or (p.get("pattern") and not re.fullmatch(p["pattern"], text)):
                    raise ValueError("invalid public identifier")
                path = path.replace("{" + p["wire"] + "}", urllib.parse.quote(text, safe=""))
            elif p["in"] == "query":
                query.append((p["wire"], text))
            elif p["in"] == "header":
                if not _SAFE_HEADER.fullmatch(text):
                    raise ValueError(f"invalid {p['name']}")
                headers[p["wire"]] = text
        if "Idempotency-Key" in headers and not _KEY.fullmatch(headers["Idempotency-Key"]):
            raise ValueError("idempotency key must be 16–128 safe characters")
        if body is not None:
            headers["Content-Type"] = spec["bodyType"]
        target = self.base + path
        if query:
            target += "?" + urllib.parse.urlencode(query)
        response = self.transport.request(target, method=spec["method"], headers=headers, body=body, cancel=cancel)
        try:
            binary = spec["responseType"] not in ("", "application/json")
            maximum = 536_870_912 if binary else 25_165_824
            raw: bytes = response.read(maximum + 1)
            if len(raw) > maximum:
                raise ValueError("Platform response exceeds bound")
            request_id = response.headers.get("X-Request-ID", "")
            metadata = {"etag": response.headers.get("ETag", ""), "request_id": request_id if re.fullmatch(r"[!-~]{1,128}", request_id) else ""}
            if response.status not in spec["statuses"]:
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
            if response.status in spec["emptyStatuses"]:
                return {"data": None, **metadata}
            if binary:
                if not response.headers.get("Content-Type", "").startswith(spec["responseType"]):
                    raise ValueError("invalid Platform response media type")
                return {"data": raw, **metadata}
            if not response.headers.get("Content-Type", "").startswith("application/json"):
                raise ValueError("invalid Platform response media type")
            return {"data": json.loads(raw), **metadata}
        finally:
            response.close()


__all__ = ["APIError", "PlatformClient", "Profile", "resource_for", "wait_for", "walk_audit_events"]


def walk_audit_events(client: PlatformClient, visit: Callable[[list[Any] | None], None], limit: int = 100, max_pages: int = 100, before: str = "", cancel: threading.Event | None = None) -> str:
    """Traverse at most 100 Platform audit keysets using the opaque next_before cursor."""
    if not 1 <= limit <= 500 or not 1 <= max_pages <= 100:
        raise ValueError("audit pagination bounds invalid")
    for _ in range(max_pages):
        if cancel is not None and cancel.is_set():
            raise TimeoutError("audit walk cancelled")
        request: dict[str, Any] = {"limit": limit}
        if before:
            request["before"] = before
        page = client._call("listAuditEvents", request, cancel)
        visit(page["events"])
        next_before = page["next_before"]
        if not next_before:
            return ""
        if next_before == before:
            raise ValueError("Platform audit cursor did not advance")
        before = next_before
    return before


def wait_for[T](fetch: Callable[[threading.Event], T], terminal: Callable[[T], bool], timeout: float, cancel: threading.Event | None = None) -> T:
    """Poll a GET callback for 1–120 seconds; pass the event into MachineClient.request."""
    if not 1 <= timeout <= 120:
        raise ValueError("poll timeout must be 1s..2m")
    signal = threading.Event()
    done = threading.Event()
    timer = threading.Timer(timeout, signal.set)
    timer.daemon = True
    timer.start()
    if cancel is not None:
        def relay() -> None:
            while not done.wait(0.05):
                if cancel.is_set():
                    signal.set()
                    return
        threading.Thread(target=relay, daemon=True).start()
        if cancel.is_set():
            signal.set()
    try:
        while not signal.is_set():
            result = fetch(signal)
            if signal.is_set():
                break
            if terminal(result):
                return result
            signal.wait(1)
        raise TimeoutError("Platform poll cancelled or timed out")
    finally:
        done.set()
        timer.cancel()
