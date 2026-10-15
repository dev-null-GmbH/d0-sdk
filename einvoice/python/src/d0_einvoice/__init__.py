"""Seven validation-only EInvoice operations backed by the shared DPoP client."""

from __future__ import annotations

import base64
import hashlib
import json
import math
import re
import threading
import time
import urllib.parse
from typing import Any, Literal, NotRequired, TypedDict, cast

from d0_auth_machine import MachineClient
from joserfc.jwk import RSAKey

Profile = Literal["production", "test"]
ValidationStatus = Literal["queued", "running", "succeeded", "failed"]


def resource_for(profile: Profile) -> str:
    if profile == "production":
        return "https://api.d0.eu/einvoice"
    if profile == "test":
        return "https://api.test.d0.eu/einvoice"
    raise ValueError("unsupported EInvoice profile")


class ByteIdentity(TypedDict):
    sizeBytes: int
    sha256: str
    contentDigest: str


class Document(TypedDict):
    schema: str
    id: str
    mediaType: str
    byteIdentity: ByteIdentity
    createdAt: str
    expiresAt: str


class ValidationOperation(TypedDict):
    schema: str
    id: str
    documentId: str
    validationPolicyId: str
    status: ValidationStatus
    requestedAt: str
    updatedAt: str
    startedAt: NotRequired[str]
    completedAt: NotRequired[str]
    resultId: NotRequired[str]
    resultUri: NotRequired[str]
    failure: NotRequired[dict[str, str]]


class ValidationPolicy(TypedDict):
    schema: str
    id: str
    name: str
    version: str
    status: str
    manifestSha256: str
    manifestContentDigest: str
    acceptedSyntaxes: list[str]
    profiles: list[str]
    validator: dict[str, Any]
    rulesets: list[dict[str, Any]]
    publishedAt: str
    description: NotRequired[str]


class PolicyPage(TypedDict):
    schema: str
    items: list[ValidationPolicy]
    nextCursor: NotRequired[str]


class ValidationResult(TypedDict):
    schema: str
    id: str
    operationId: str
    source: dict[str, Any]
    validationPolicy: dict[str, Any]
    valid: bool
    syntax: str
    validatedAt: str
    evidence: dict[str, Any]
    issues: list[dict[str, Any]]
    profile: NotRequired[str]


class APIError(Exception):
    """Safe bounded problem metadata. No raw body or invoice content."""

    def __init__(
        self, status: int, problem_type: str = "", title: str = "", request_id: str = ""
    ) -> None:
        super().__init__(f"EInvoice request failed (HTTP {status})")
        self.status = status
        self.type = problem_type
        self.title = title
        self.request_id = request_id


_ID = re.compile(r"^(?:doc_|vop_|vpol_)[A-Za-z0-9]{20,80}$")
_KEY = re.compile(r"^[A-Za-z0-9._~:+/=-]{16,128}$")
_REQUEST_ID = re.compile(r"^[!-~]{1,128}$")


def _identifier(value: str, prefix: str) -> str:
    if not isinstance(value, str) or not value.startswith(prefix) or not _ID.fullmatch(value):
        raise ValueError("invalid EInvoice identifier")
    return value


def _key(value: str) -> str:
    if not isinstance(value, str) or not _KEY.fullmatch(value):
        raise ValueError("idempotency key must be 16–128 contract-safe characters")
    return value


class EInvoiceClient:
    """Fixed-profile product methods; MachineClient handles OAuth and DPoP."""

    def __init__(self, profile: Profile, transport: MachineClient) -> None:
        self.base = resource_for(profile) + "/v1"
        if not isinstance(transport, MachineClient):
            raise TypeError("shared MachineClient required")
        if transport.resource != resource_for(profile):
            raise ValueError("machine client resource does not match profile")
        self._transport = transport

    def _call(
        self,
        path: str,
        expected: int,
        *,
        method: str = "GET",
        key: str = "",
        media: str = "",
        body: bytes | None = None,
        digest: str = "",
        cancel: threading.Event | None = None,
        timeout: float = 45.0,
        retry: list[float] | None = None,
    ) -> dict[str, Any]:
        headers = {"Accept": "application/json"}
        if key:
            headers["Idempotency-Key"] = key
        if media:
            headers["Content-Type"] = media
        if digest:
            headers["Content-Digest"] = digest
        response = self._transport.request(
            self.base + path,
            method=method,
            headers=headers,
            body=body,
            cancel=cancel,
            timeout=timeout,
        )
        try:
            raw = response.read((24 << 20) + 1)
            if len(raw) > 24 << 20:
                raise ValueError("oversized EInvoice response")
            if response.status != expected:
                problem: dict[str, Any] = {}
                try:
                    if response.headers.get("Content-Type", "").startswith(
                        "application/problem+json"
                    ):
                        decoded = json.loads(raw)
                        if isinstance(decoded, dict) and decoded.get("status") == response.status:
                            problem = decoded
                except (ValueError, UnicodeDecodeError):
                    pass
                problem_type = problem.get("type", "")
                if (
                    not isinstance(problem_type, str)
                    or len(problem_type) > 2048
                    or not problem_type.startswith(
                        "https://api.d0.eu/einvoice/problems/"
                    )
                ):
                    problem_type = ""
                title = problem.get("title", "")
                if not isinstance(title, str) or len(title) > 256:
                    title = ""
                request_id = response.headers.get("X-Request-ID", "")
                if not _REQUEST_ID.fullmatch(request_id):
                    request_id = ""
                raise APIError(response.status, problem_type, title, request_id)
            if not response.headers.get("Content-Type", "").startswith(
                "application/json"
            ):
                raise ValueError("invalid EInvoice response")
            decoded = json.loads(raw)
            if not isinstance(decoded, dict):
                raise TypeError("invalid EInvoice response")
            if retry is not None:
                raw_delay = response.headers.get("Retry-After", "")
                if re.fullmatch(r"(?:[1-9]|[1-9][0-9]|[12][0-9]{2}|300)", raw_delay):
                    retry[:] = [float(raw_delay)]
                else:
                    retry[:] = [1.0]
            return decoded
        except (ValueError, TypeError, UnicodeDecodeError):
            raise ValueError("invalid EInvoice response") from None
        finally:
            response.close()

    def create_document(
        self,
        xml: bytes | bytearray,
        idempotency_key: str,
        *,
        cancel: threading.Event | None = None,
    ) -> Document:
        _key(idempotency_key)
        if not isinstance(xml, (bytes, bytearray)) or not 1 <= len(xml) <= 20_971_520:
            raise ValueError("invalid XML byte length")
        body = bytes(xml)
        digest = "sha-256=:" + base64.b64encode(hashlib.sha256(body).digest()).decode() + ":"
        return cast(
            Document,
            self._call(
                "/documents", 201, method="POST", key=idempotency_key,
                media="application/xml", body=body, digest=digest, cancel=cancel,
            ),
        )

    def get_document(self, document_id: str, *, cancel: threading.Event | None = None) -> Document:
        return cast(Document, self._call("/documents/" + _identifier(document_id, "doc_"), 200, cancel=cancel))

    def create_validation_operation(
        self, document_id: str, policy_id: str, idempotency_key: str,
        *, cancel: threading.Event | None = None,
    ) -> ValidationOperation:
        _identifier(document_id, "doc_")
        _identifier(policy_id, "vpol_")
        _key(idempotency_key)
        body = json.dumps(
            {"documentId": document_id, "validationPolicyId": policy_id},
            separators=(",", ":"),
        ).encode()
        return cast(
            ValidationOperation,
            self._call(
                "/validation-operations", 202, method="POST", key=idempotency_key,
                media="application/json", body=body, cancel=cancel,
            ),
        )

    def get_validation_operation(
        self, operation_id: str, *, cancel: threading.Event | None = None,
        timeout: float = 45.0,
    ) -> ValidationOperation:
        return self._get_validation_operation(operation_id, cancel=cancel, timeout=timeout)

    def _get_validation_operation(
        self, operation_id: str, *, cancel: threading.Event | None = None,
        timeout: float = 45.0, retry: list[float] | None = None,
    ) -> ValidationOperation:
        path = "/validation-operations/" + _identifier(operation_id, "vop_")
        return cast(ValidationOperation, self._call(path, 200, cancel=cancel, timeout=timeout, retry=retry))

    def get_validation_result(
        self, operation_id: str, *, cancel: threading.Event | None = None,
    ) -> ValidationResult:
        path = "/validation-operations/" + _identifier(operation_id, "vop_") + "/result"
        return cast(ValidationResult, self._call(path, 200, cancel=cancel))

    def list_validation_policies(
        self, limit: int = 50, cursor: str = "", *, cancel: threading.Event | None = None,
    ) -> PolicyPage:
        if type(limit) is not int or not 1 <= limit <= 100 or not isinstance(cursor, str) or len(cursor) > 1024:
            raise ValueError("invalid policy page")
        query = urllib.parse.urlencode({"limit": limit, **({"cursor": cursor} if cursor else {})})
        return cast(PolicyPage, self._call("/validation-policies?" + query, 200, cancel=cancel))

    def get_validation_policy(
        self, policy_id: str, *, cancel: threading.Event | None = None,
    ) -> ValidationPolicy:
        return cast(ValidationPolicy, self._call("/validation-policies/" + _identifier(policy_id, "vpol_"), 200, cancel=cancel))

    def wait_validation(
        self, operation_id: str, max_wait: float,
        *, cancel: threading.Event | None = None,
    ) -> ValidationOperation:
        _identifier(operation_id, "vop_")
        if type(max_wait) not in (float, int) or not math.isfinite(max_wait) or not 0 < max_wait <= 120:
            raise ValueError("poll limit must be within two minutes")
        deadline = time.monotonic() + max_wait
        while True:
            if cancel is not None and cancel.is_set():
                raise TimeoutError("validation poll cancelled")
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("validation poll timed out")
            retry = [1.0]
            operation = self._get_validation_operation(
                operation_id, cancel=cancel, timeout=min(remaining, 45.0), retry=retry,
            )
            if operation["status"] in ("succeeded", "failed"):
                return operation
            if operation["status"] not in ("queued", "running"):
                raise ValueError("invalid validation state")
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("validation poll timed out")
            if cancel is not None:
                if cancel.wait(min(retry[0], remaining)):
                    raise TimeoutError("validation poll cancelled")
            else:
                time.sleep(min(retry[0], remaining))


def create_client(
    profile: Profile,
    *,
    client_id: str,
    key_id: str,
    signing_key: RSAKey,
    scopes: list[str] | tuple[str, ...],
) -> EInvoiceClient:
    transport = MachineClient(
        client_id=client_id, key_id=key_id, signing_key=signing_key,
        resource=resource_for(profile), scopes=scopes,
    )
    return EInvoiceClient(profile, transport)


__all__ = [
    "APIError", "ByteIdentity", "Document", "EInvoiceClient", "PolicyPage",
    "Profile", "ValidationOperation", "ValidationPolicy", "ValidationResult",
    "create_client", "resource_for",
]
