"""Server-side d0 client-credentials and DPoP HTTP transport."""

from __future__ import annotations

import base64
import concurrent.futures
import hashlib
import json
import math
import re
import ssl
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from collections.abc import Mapping
from http.client import HTTPException
from typing import Any, cast

from joserfc import jwt
from joserfc.jwk import ECKey, RSAKey

_ISSUER = "https://auth.d0.eu"
_TOKEN_ENDPOINT = _ISSUER + "/oauth2/token"
_RESOURCES = {
    f"{origin}/{name}": name
    for origin in ("https://api.d0.eu", "https://api.test.d0.eu")
    for name in ("platform", "accounting", "einvoice", "eric")
}
_FORBIDDEN_HEADERS = {
    "authorization",
    "dpop",
    "host",
    "cookie",
    "proxy-authorization",
    "content-length",
    "transfer-encoding",
}
_FORBIDDEN_QUERY = {
    "access_token",
    "authorization",
    "dpop",
    "client_assertion",
    "client_secret",
    "refresh_token",
    "api_key",
    "apikey",
    "token",
    "password",
    "secret",
}
_BAD_PATH_ENCODING = re.compile(r"%(?:2e|2f|5c|25|00)", re.IGNORECASE)


def _safe(value: object, maximum: int) -> bool:
    return (
        isinstance(value, str)
        and 0 < len(value) <= maximum
        and all("!" <= ch <= "~" for ch in value)
    )


def _header_values(headers: Any, name: str) -> list[str]:
    if hasattr(headers, "get_all"):
        return cast(list[str], headers.get_all(name, []))
    return [value for key, value in headers.items() if key.lower() == name.lower()]


def _nonce(headers: Any) -> str:
    values = _header_values(headers, "DPoP-Nonce")
    return (
        values[0]
        if len(values) == 1 and _safe(values[0], 512) and "," not in values[0]
        else ""
    )


def _json_object(raw: bytes) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result

    result = json.loads(raw, object_pairs_hook=unique)
    if not isinstance(result, dict):
        raise TypeError("JSON object required")
    return result


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self,
        request: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        return None


class MachineClient:
    """One organization's client for one d0 product resource.

    Requests use locally held signing material and never follow redirects.
    Product contracts define idempotency requirements; bodies must be replayable.
    """

    def __init__(
        self,
        client_id: str,
        key_id: str,
        signing_key: RSAKey,
        resource: str,
        scopes: list[str] | tuple[str, ...],
    ):
        if (
            resource not in _RESOURCES
            or not _safe(client_id, 128)
            or not _safe(key_id, 128)
        ):
            raise ValueError("invalid d0 resource, client ID or key ID")
        if (
            not isinstance(signing_key, RSAKey)
            or not signing_key.is_private
            or signing_key.raw_value.key_size < 3072
        ):
            raise ValueError(
                "a private RSA signing key of at least 3072 bits is required"
            )
        try:
            ordered = tuple(sorted(scopes))
        except TypeError, ValueError:
            raise ValueError("invalid scopes") from None
        if (
            not 1 <= len(ordered) <= 64
            or any(
                not _safe(scope, 128)
                or not scope.startswith(_RESOURCES[resource] + ".")
                for scope in ordered
            )
            or len(set(ordered)) != len(ordered)
        ):
            raise ValueError("invalid, duplicate or foreign resource scope")
        self.client_id, self.key_id, self.signing_key = client_id, key_id, signing_key
        self.resource, self.scopes = resource, ordered
        self._proof_key = ECKey.generate_key("P-256")
        self._proof_public = self._proof_key.as_dict(private=False)
        self._state_lock = threading.Lock()
        self._refresh: concurrent.futures.Future[str] | None = None
        self._token = ""
        self._expires = 0.0
        self._as_nonce = ""
        self._api_nonce = ""
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_3
        self._opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}),
            urllib.request.HTTPSHandler(context=context),
            _NoRedirect(),
        )

    def _send(self, request: urllib.request.Request, timeout: float) -> Any:
        try:
            return self._opener.open(request, timeout=timeout)
        except urllib.error.HTTPError as response:
            return response

    @staticmethod
    def _check(cancel: threading.Event | None, deadline: float) -> None:
        if cancel is not None and cancel.is_set():
            raise TimeoutError("d0 request canceled")
        if time.monotonic() >= deadline:
            raise TimeoutError("d0 request timed out")

    def _perform(self, request: urllib.request.Request, timeout: float) -> Any:
        try:
            return self._send(request, max(0.001, timeout))
        except TimeoutError:
            raise TimeoutError("d0 request timed out") from None
        except OSError, urllib.error.URLError, HTTPException:
            raise RuntimeError(
                "d0 transport failed; preserve the original operation and idempotency key after an uncertain outcome"
            ) from None

    def _proof(self, method: str, url: str, nonce: str, token: str = "") -> str:
        parsed = urllib.parse.urlsplit(url)
        claims: dict[str, Any] = {
            "htm": method,
            "htu": f"{parsed.scheme}://{parsed.netloc}{parsed.path}",
            "iat": int(time.time()),
            "jti": str(uuid.uuid4()),
        }
        if nonce:
            claims["nonce"] = nonce
        if token:
            claims["ath"] = (
                base64.urlsafe_b64encode(hashlib.sha256(token.encode("ascii")).digest())
                .rstrip(b"=")
                .decode("ascii")
            )
        try:
            return jwt.encode(
                {"alg": "ES256", "typ": "dpop+jwt", "jwk": self._proof_public},
                claims,
                self._proof_key,
                algorithms=["ES256"],
            )
        except Exception:  # noqa: BLE001 - JOSE exceptions must not expose signing material
            raise RuntimeError("could not sign DPoP proof") from None

    def _fetch_token(self) -> str:
        deadline = time.monotonic() + 10
        for attempt in range(2):
            if time.monotonic() >= deadline:
                raise TimeoutError("d0 token request timed out")
            now = int(time.time())
            try:
                assertion = jwt.encode(
                    {"alg": "PS256", "typ": "JWT", "kid": self.key_id},
                    {
                        "iss": self.client_id,
                        "sub": self.client_id,
                        "aud": _ISSUER,
                        "iat": now,
                        "exp": now + 60,
                        "jti": str(uuid.uuid4()),
                    },
                    self.signing_key,
                    algorithms=["PS256"],
                )
            except Exception:  # noqa: BLE001 - JOSE exceptions must not expose signing material
                raise RuntimeError("could not sign client assertion") from None
            body = urllib.parse.urlencode(
                {
                    "grant_type": "client_credentials",
                    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                    "client_assertion": assertion,
                    "resource": self.resource,
                    "scope": " ".join(self.scopes),
                }
            ).encode("ascii")
            request = urllib.request.Request(
                _TOKEN_ENDPOINT,
                data=body,
                method="POST",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                    "DPoP": self._proof("POST", _TOKEN_ENDPOINT, self._as_nonce),
                },
            )
            response = self._perform(request, min(10, deadline - time.monotonic()))
            try:
                try:
                    raw = response.read(32769)
                except OSError, HTTPException:
                    raise RuntimeError("d0 token response transport failed") from None
                if len(raw) > 32768:
                    raise ValueError("invalid token response size")
                try:
                    result = _json_object(raw)
                except TypeError, ValueError, UnicodeDecodeError:
                    raise ValueError("invalid token response") from None
                fresh = _nonce(response.headers)
                if fresh:
                    self._as_nonce = fresh
                if response.status != 200:
                    if (
                        attempt == 0
                        and response.status == 400
                        and fresh
                        and result.get("error") == "use_dpop_nonce"
                    ):
                        continue
                    raise ValueError(
                        f"d0 token request rejected (HTTP {response.status})"
                    )
                scope = result.get("scope")
                lifetime = result.get("expires_in")
                if (
                    not _safe(result.get("access_token"), 16384)
                    or result.get("token_type") != "DPoP"
                    or type(lifetime) is not int
                    or not 1 <= lifetime <= 300
                    or not isinstance(scope, str)
                    or tuple(sorted(scope.split(" "))) != self.scopes
                ):
                    raise ValueError("invalid DPoP token response")
                with self._state_lock:
                    self._token, self._expires = (
                        result["access_token"],
                        time.monotonic() + lifetime,
                    )
                return cast(str, result["access_token"])
            finally:
                response.close()
        raise ValueError("authorization nonce retry exhausted")

    def _access_token(self, cancel: threading.Event | None, deadline: float) -> str:
        self._check(cancel, deadline)
        with self._state_lock:
            if self._token and self._expires - time.monotonic() > 30:
                return self._token
            if self._refresh is None:
                future: concurrent.futures.Future[str] = concurrent.futures.Future()
                self._refresh = future

                def refresh() -> None:
                    try:
                        future.set_result(self._fetch_token())
                    except Exception as error:  # noqa: BLE001 - wake every waiter on any refresh failure
                        future.set_exception(error)
                    finally:
                        with self._state_lock:
                            self._refresh = None

                threading.Thread(target=refresh, daemon=True).start()
            pending = self._refresh
        while True:
            self._check(cancel, deadline)
            try:
                return pending.result(timeout=min(0.05, deadline - time.monotonic()))
            except concurrent.futures.TimeoutError:
                # Future.result also raises the refresh task's own TimeoutError.
                if pending.done():
                    return pending.result()
                continue

    def request(
        self,
        url: str,
        *,
        method: str = "GET",
        headers: Mapping[str, str] | None = None,
        body: str | bytes | bytearray | None = None,
        cancel: threading.Event | None = None,
        timeout: float = 45.0,
    ) -> Any:
        """Return a streaming urllib response; the caller must close it."""
        if (
            not isinstance(url, str)
            or not url.isascii()
            or any(not "!" <= ch <= "~" for ch in url)
            or re.search(r"%(?![0-9a-fA-F]{2})", url)
        ):
            raise ValueError("invalid API URL")
        try:
            parsed = urllib.parse.urlsplit(url)
            query = urllib.parse.parse_qsl(
                parsed.query, keep_blank_values=True, strict_parsing=False
            )
        except ValueError:
            raise ValueError("invalid API URL") from None
        prefix = f"/{_RESOURCES[self.resource]}/v1"
        if (
            parsed.scheme != "https"
            or parsed.netloc != urllib.parse.urlsplit(self.resource).netloc
            or parsed.fragment
            or not (parsed.path == prefix or parsed.path.startswith(prefix + "/"))
            or "//" in parsed.path
            or "/." in parsed.path
            or "\\" in parsed.path
            or _BAD_PATH_ENCODING.search(parsed.path)
        ):
            raise ValueError("request is outside the configured canonical resource")
        if any(name.lower() in _FORBIDDEN_QUERY for name, _ in query):
            raise ValueError("credentials are forbidden in request queries")
        if not isinstance(method, str) or method not in {
            "GET",
            "HEAD",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
        }:
            raise ValueError("unsupported API method")
        supplied: dict[str, str] = {}
        original_headers: dict[str, str] = {}
        for name, value in (headers or {}).items():
            if (
                not isinstance(name, str)
                or not isinstance(value, str)
                or not re.fullmatch(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+", name)
                or any(ch in value for ch in "\r\n\x00")
            ):
                raise ValueError("invalid request header")
            lowered = name.lower()
            if lowered in supplied or lowered in _FORBIDDEN_HEADERS:
                raise ValueError(
                    "caller-provided credentials or transport overrides are forbidden"
                )
            supplied[lowered] = value
            original_headers[name] = value
        if "idempotency-key" in supplied and not _safe(
            supplied["idempotency-key"], 128
        ):
            raise ValueError("invalid Idempotency-Key")
        if method in {"GET", "HEAD"} and body is not None:
            raise ValueError("read requests cannot carry a body")
        if not isinstance(body, (str, bytes, bytearray, type(None))):
            raise TypeError("request body must be replayable bytes or a string")
        data = (
            body.encode("utf-8")
            if isinstance(body, str)
            else bytes(body)
            if body is not None
            else None
        )
        if (
            type(timeout) not in (int, float)
            or not math.isfinite(timeout)
            or not 0 < timeout <= 45
        ):
            raise ValueError("timeout must be between 0 and 45 seconds")
        deadline = time.monotonic() + timeout
        token = self._access_token(cancel, deadline)
        for attempt in range(2):
            self._check(cancel, deadline)
            with self._state_lock:
                nonce = self._api_nonce
            request = urllib.request.Request(
                url, data=data, method=method, headers=original_headers
            )
            request.add_header("Authorization", "DPoP " + token)
            request.add_header("DPoP", self._proof(method, url, nonce, token))
            response = self._perform(request, deadline - time.monotonic())
            fresh = _nonce(response.headers)
            if fresh:
                with self._state_lock:
                    self._api_nonce = fresh
            if 300 <= response.status < 400 and response.status != 304:
                response.close()
                raise ValueError("authenticated API redirects are forbidden")
            if (
                attempt == 0
                and response.status == 401
                and fresh
                and any(
                    re.search(r'^DPoP\s+.*\berror="use_dpop_nonce"', value)
                    for value in _header_values(response.headers, "WWW-Authenticate")
                )
            ):
                response.close()
                continue
            return response
        raise ValueError("DPoP nonce retry exhausted")


__all__ = ["MachineClient"]
