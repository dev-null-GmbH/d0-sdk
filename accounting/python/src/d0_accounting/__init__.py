"""Typed Accounting machine operations; OAuth and DPoP use d0-auth-machine."""
from __future__ import annotations

import json
import re
import threading
import time
import urllib.parse
from collections.abc import Callable, Mapping
from typing import Any, Literal

from d0_auth_machine import MachineClient
from joserfc.jwk import RSAKey

from .methods import AccountingOperations
from .operations import OPERATIONS

Profile = Literal["production", "test"]


def resource_for(profile: Profile) -> str:
    if profile == "production":
        return "https://api.d0.eu/accounting"
    if profile == "test":
        return "https://api.test.d0.eu/accounting"
    raise ValueError("unsupported Accounting profile")


class APIError(Exception):
    def __init__(self, status: int, problem_type: str = "", title: str = "", request_id: str = ""):
        super().__init__(f"Accounting request failed (HTTP {status})")
        self.status = status
        self.type = problem_type
        self.title = title
        self.request_id = request_id


_TENANT = re.compile(r"^ten_[0-9A-HJKMNP-TV-Z]{26}$")
_KEY = re.compile(r"^[!-~]{16,128}$")
_SAFE_ID = re.compile(r"^[A-Za-z0-9_-]{1,128}$")
_SAFE_HEADER = re.compile(r"^[!-~]{1,256}$")


def _exact_money(value: Any) -> None:
    if isinstance(value, list):
        for item in value:
            _exact_money(item)
    elif isinstance(value, dict):
        if "amount" in value and "currency" in value and (not isinstance(value["amount"], str) or not re.fullmatch(r"-?(0|[1-9][0-9]{0,18})", value["amount"])):
            raise ValueError("Accounting amounts must be exact minor-unit decimal strings")
        for item in value.values():
            _exact_money(item)


class AccountingClient(AccountingOperations):
    def __init__(self, profile: Profile, tenant: str, transport: MachineClient):
        if tenant and not _TENANT.fullmatch(tenant):
            raise ValueError("invalid public tenant ID")
        if not isinstance(transport, MachineClient) or transport.resource != resource_for(profile):
            raise ValueError("shared machine client resource does not match Accounting profile")
        self.profile = profile
        self.tenant = tenant
        self.base = resource_for(profile) + "/v1"
        self.transport = transport
        self.last_response: dict[str, str] = {"etag": "", "request_id": ""}

    @classmethod
    def create(cls, profile: Profile, tenant: str, client_id: str, key_id: str, signing_key: RSAKey, scopes: list[str]) -> AccountingClient:
        return cls(profile, tenant, MachineClient(client_id, key_id, signing_key, resource_for(profile), scopes))

    def _call(self, operation: str, request: Mapping[str, Any], cancel: threading.Event | None = None) -> Any:
        return self.call_with_response(operation, request, cancel)["data"]

    def call_with_response(self, operation: str, request: Mapping[str, Any], cancel: threading.Event | None = None) -> dict[str, Any]:
        """Return the result and its own ETag/request ID; safe for concurrent calls."""
        spec = OPERATIONS.get(operation)
        if spec is None:
            raise ValueError("unknown Accounting operation")
        if self.profile == "test" and not spec["test"]:
            raise ValueError("operation unavailable in Accounting test environment")
        if not self.tenant and operation not in ("listTenants", "createTenant"):
            raise ValueError("selected public tenant ID required")
        known = {p["name"] for p in spec["params"]}
        if request.keys() - known:
            raise ValueError("unknown Accounting request field")
        path = spec["path"]
        query: list[tuple[str, str]] = []
        headers = {"X-Accounting-Tenant": self.tenant} if self.tenant else {}
        body: bytes | None = None
        for p in spec["params"]:
            value = request.get(p["name"])
            if value is None:
                if p["required"]:
                    raise ValueError(f"required {p['name']} missing")
                continue
            if p["in"] == "body":
                _exact_money(value)
                body = json.dumps(value, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
                continue
            if not isinstance(value, (str, int, bool)) or isinstance(value, float):
                raise TypeError(f"invalid {p['name']}")
            text = str(value).lower() if isinstance(value, bool) else str(value)
            if p["in"] == "path":
                if not _SAFE_ID.fullmatch(text) or (p.get("pattern") and not re.fullmatch(p["pattern"], text)):
                    raise ValueError("invalid public identifier")
                path = path.replace("{" + p["wire"] + "}", urllib.parse.quote(text, safe=""))
            elif p["in"] == "query":
                query.append((p["wire"], text))
            elif p["in"] == "header":
                if not _SAFE_HEADER.fullmatch(text):
                    raise ValueError(f"invalid {p['name']}")
                headers[p["wire"]] = text
        if spec["method"] != "GET" and not _KEY.fullmatch(headers.get("Idempotency-Key", "")):
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
                raise ValueError("Accounting response exceeds bound")
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
            if response.status == 204:
                return {"data": None, **metadata}
            if binary:
                if not response.headers.get("Content-Type", "").startswith(spec["responseType"]):
                    raise ValueError("invalid Accounting response media type")
                return {"data": raw, **metadata}
            if not response.headers.get("Content-Type", "").startswith("application/json"):
                raise ValueError("invalid Accounting response media type")
            return {"data": json.loads(raw), **metadata}
        finally:
            response.close()


__all__ = ["APIError", "AccountingClient", "Profile", "resource_for", "wait_for", "walk_pages"]


def walk_pages[T](fetch: Callable[[int, str], dict[str, Any]], visit: Callable[[list[T]], None], limit: int = 100, max_pages: int = 100, after: str = "") -> str:
    """Visit up to max_pages without interpreting opaque cursors; return continuation."""
    if not 1 <= limit <= 100 or not 1 <= max_pages <= 100:
        raise ValueError("pagination bounds must be 1..100")
    for _ in range(max_pages):
        page = fetch(limit, after)
        visit(page["data"])
        next_cursor = page.get("nextCursor", "")
        if not next_cursor:
            return ""
        if next_cursor == after:
            raise ValueError("Accounting cursor did not advance")
        after = next_cursor
    return after


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
    raise TimeoutError("Accounting poll cancelled or timed out")
