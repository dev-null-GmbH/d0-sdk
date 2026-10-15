import base64
import hashlib
import json
import threading
import time
import unittest
from urllib.parse import parse_qs

from joserfc import jwt
from joserfc.jwk import ECKey, RSAKey

from d0_auth_machine import MachineClient


class FakeResponse:
    def __init__(self, status=200, body=b"", headers=None):
        self.status = status
        self.body = body
        self.headers = headers or {}
        self.closed = False

    def read(self, size=-1):
        if size < 0:
            size = len(self.body)
        result, self.body = self.body[:size], self.body[size:]
        return result

    def close(self):
        self.closed = True


class MachineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key = RSAKey.generate_key(3072)

    def client(self, resource="https://api.d0.eu/platform"):
        return MachineClient(
            "fixture-client",
            "fixture-key",
            self.key,
            resource,
            ["platform.domains.read"],
        )

    def test_rejects_weak_key_and_foreign_scope(self):
        with self.assertRaisesRegex(ValueError, "3072"):
            MachineClient(
                "fixture",
                "key",
                RSAKey.generate_key(2048),
                "https://api.d0.eu/platform",
                ["platform.domains.read"],
            )
        for scopes in (
            ["accounting.documents.read"],
            ["platform.domains.read"] * 2,
            [],
        ):
            with self.subTest(scopes=scopes), self.assertRaises(ValueError):
                MachineClient(
                    "fixture", "key", self.key, "https://api.d0.eu/platform", scopes
                )

    def test_both_nonces_signed_and_exact_replay(self):
        client = self.client()
        seen = set()
        calls = []

        def network(request, timeout):
            headers = dict(request.header_items())
            url = request.full_url
            proof_header = json.loads(
                base64.urlsafe_b64decode(headers["Dpop"].split(".")[0] + "==")
            )
            self.assertEqual(proof_header["alg"], "ES256")
            self.assertEqual(proof_header["typ"], "dpop+jwt")
            self.assertNotIn("d", proof_header["jwk"])
            proof = jwt.decode(
                headers["Dpop"],
                ECKey.import_key(proof_header["jwk"], parameters={"alg": "ES256"}),
                algorithms=["ES256"],
            )
            self.assertEqual(proof.claims["htu"], url.split("?")[0])
            self.assertEqual(proof.claims["htm"], request.get_method())
            self.assertNotIn(proof.claims["jti"], seen)
            seen.add(proof.claims["jti"])
            calls.append((url, request.data, headers, proof.claims))
            if url.endswith("/oauth2/token"):
                form = parse_qs(request.data.decode())
                assertion = jwt.decode(
                    form["client_assertion"][0], self.key, algorithms=["PS256"]
                )
                self.assertEqual(assertion.header["alg"], "PS256")
                self.assertEqual(assertion.header["kid"], "fixture-key")
                self.assertEqual(assertion.claims["aud"], "https://auth.d0.eu")
                self.assertEqual(assertion.claims["exp"] - assertion.claims["iat"], 60)
                self.assertEqual(form["resource"], ["https://api.d0.eu/platform"])
                self.assertEqual(form["scope"], ["platform.domains.read"])
                self.assertNotIn(assertion.claims["jti"], seen)
                seen.add(assertion.claims["jti"])
                if len(calls) == 1:
                    return FakeResponse(
                        400, b'{"error":"use_dpop_nonce"}', {"DPoP-Nonce": "as-nonce"}
                    )
                self.assertEqual(proof.claims["nonce"], "as-nonce")
                self.assertNotIn("ath", proof.claims)
                return FakeResponse(
                    body=b'{"access_token":"fixture-token","token_type":"DPoP","expires_in":300,"scope":"platform.domains.read"}'
                )
            self.assertEqual(headers["Authorization"], "DPoP fixture-token")
            self.assertEqual(
                proof.claims["ath"],
                base64.urlsafe_b64encode(hashlib.sha256(b"fixture-token").digest())
                .rstrip(b"=")
                .decode(),
            )
            if len(calls) == 3:
                return FakeResponse(
                    401,
                    b"",
                    {
                        "DPoP-Nonce": "api-nonce",
                        "WWW-Authenticate": 'DPoP error="use_dpop_nonce"',
                    },
                )
            self.assertEqual(proof.claims["nonce"], "api-nonce")
            return FakeResponse(201)

        client._send = network
        response = client.request(
            "https://api.d0.eu/platform/v1/domains?limit=1",
            method="POST",
            headers={"Idempotency-Key": "stable", "If-Match": '"one"'},
            body=b'{"unchanged":true}',
        )
        self.assertEqual(response.status, 201)
        self.assertEqual(len(seen), 6)
        self.assertEqual(calls[2][1], calls[3][1])
        self.assertEqual(calls[2][2]["Idempotency-key"], calls[3][2]["Idempotency-key"])
        self.assertEqual(calls[2][2]["If-match"], calls[3][2]["If-match"])

    def test_signed_test_resource_uses_same_issuer_and_test_htu(self):
        resource = "https://api.test.d0.eu/platform"
        with self.assertRaises(ValueError):
            self.client("https://api.preview.d0.eu/platform")
        client = self.client(resource)
        calls = []

        def network(request, timeout):
            calls.append(request.full_url)
            headers = dict(request.header_items())
            protected = json.loads(
                base64.urlsafe_b64decode(headers["Dpop"].split(".")[0] + "==")
            )
            proof = jwt.decode(
                headers["Dpop"],
                ECKey.import_key(protected["jwk"]),
                algorithms=["ES256"],
            )
            self.assertEqual(proof.claims["htu"], request.full_url.split("?")[0])
            if request.full_url == "https://auth.d0.eu/oauth2/token":
                form = parse_qs(request.data.decode())
                assertion = jwt.decode(
                    form["client_assertion"][0], self.key, algorithms=["PS256"]
                )
                self.assertEqual(assertion.claims["aud"], "https://auth.d0.eu")
                self.assertEqual(form["resource"], [resource])
                return FakeResponse(
                    body=b'{"access_token":"fixture-token","token_type":"DPoP","expires_in":300,"scope":"platform.domains.read"}'
                )
            self.assertEqual(headers["Authorization"], "DPoP fixture-token")
            return FakeResponse(204)

        client._send = network
        response = client.request(resource + "/v1/domains")
        self.assertEqual(response.status, 204)
        self.assertEqual(
            calls, ["https://auth.d0.eu/oauth2/token", resource + "/v1/domains"]
        )

    def test_rejects_unsafe_targets_and_headers_before_network(self):
        client = self.client()
        client._send = lambda *_: self.fail("network reached")
        for url in [
            "http://api.d0.eu/platform/v1/x",
            "https://evil.invalid/platform/v1/x",
            "https://api.test.d0.eu/platform/v1/x",
            "https://api.d0.eu/accounting/v1/x",
            "https://api.d0.eu/platform/v1/../x",
            "https://api.d0.eu/platform/v1/%2e%2e/x",
            "https://api.d0.eu/platform/v1/x?access_token=secret",
            "https://api.d0.eu/platform/v1/x#fragment",
            "https://u:p@api.d0.eu/platform/v1/x",
        ]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                client.request(url)
        test_client = self.client("https://api.test.d0.eu/platform")
        test_client._send = lambda *_: self.fail("network reached")
        with self.assertRaises(ValueError):
            test_client.request("https://api.d0.eu/platform/v1/x")
        for name in [
            "Authorization",
            "DPoP",
            "Host",
            "Cookie",
            "Proxy-Authorization",
            "Transfer-Encoding",
            "Content-Length",
        ]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                client.request(
                    "https://api.d0.eu/platform/v1/x", headers={name: "secret"}
                )
        with self.assertRaises(ValueError):
            client.request(
                "https://api.d0.eu/platform/v1/x",
                method="POST",
                body=b"x",
                headers={"Idempotency-Key": ""},
            )

    def test_idempotency_requirement_belongs_to_product_contract(self):
        client = self.client()
        client._token, client._expires = "fixture-token", time.monotonic() + 300
        calls = []

        def network(request, timeout):
            self.assertIsNone(request.get_header("Idempotency-key"))
            self.assertEqual(request.data, b"{}")
            calls.append(request.get_method())
            return FakeResponse(status=204)

        client._send = network
        for method in ["POST", "PUT", "PATCH", "DELETE"]:
            response = client.request(
                "https://api.d0.eu/platform/v1/contract-operation",
                method=method,
                body=b"{}",
            )
            self.assertEqual(response.status, 204)
            response.close()
            for key in ["", "contains space", "x" * 129]:
                with self.assertRaisesRegex(ValueError, "Idempotency-Key"):
                    client.request(
                        "https://api.d0.eu/platform/v1/contract-operation",
                        method=method,
                        body=b"{}",
                        headers={"Idempotency-Key": key},
                    )
        self.assertEqual(calls, ["POST", "PUT", "PATCH", "DELETE"])

    def test_invalid_token_and_sanitized_errors(self):
        for result in [
            {
                "access_token": "secret",
                "token_type": "Bearer",
                "expires_in": 300,
                "scope": "platform.domains.read",
            },
            {
                "access_token": "secret",
                "token_type": "DPoP",
                "expires_in": 301,
                "scope": "platform.domains.read",
            },
            {
                "access_token": "secret",
                "token_type": "DPoP",
                "expires_in": 300,
                "scope": "platform.domains.write",
            },
        ]:
            client = self.client()
            client._send = lambda *_, result=result: FakeResponse(
                body=json.dumps(result).encode()
            )
            with self.assertRaises(ValueError) as caught:
                client.request("https://api.d0.eu/platform/v1/x")
            self.assertNotIn("secret", str(caught.exception))

    def test_shared_refresh(self):
        client = self.client()
        calls = []
        barrier = threading.Barrier(4)

        def network(request, timeout):
            calls.append(request.full_url)
            if request.full_url.endswith("/oauth2/token"):
                return FakeResponse(
                    body=b'{"access_token":"fixture-token","token_type":"DPoP","expires_in":300,"scope":"platform.domains.read"}'
                )
            return FakeResponse(204)

        client._send = network
        errors = []

        def worker():
            barrier.wait()
            try:
                client.request("https://api.d0.eu/platform/v1/x")
            except Exception as error:  # noqa: BLE001 - collect failures across test threads
                errors.append(error)

        threads = [threading.Thread(target=worker) for _ in range(3)]
        for thread in threads:
            thread.start()
        barrier.wait()
        for thread in threads:
            thread.join()
        self.assertEqual(errors, [])
        self.assertEqual(sum(url.endswith("/oauth2/token") for url in calls), 1)

    def test_refresh_timeout_is_returned_to_waiters(self):
        client = self.client()

        def fetch_token():
            raise TimeoutError("d0 token request timed out")

        client._fetch_token = fetch_token
        with self.assertRaisesRegex(TimeoutError, "d0 token request timed out"):
            client.request("https://api.d0.eu/platform/v1/x", timeout=0.1)

    def test_timeout_is_a_finite_number(self):
        client = self.client()
        client._send = lambda *_: self.fail("network reached")
        for timeout in (float("nan"), float("inf"), -float("inf"), True, 0, 46):
            with self.subTest(timeout=timeout), self.assertRaises(ValueError):
                client.request("https://api.d0.eu/platform/v1/x", timeout=timeout)

    def test_cancelled_caller_does_not_cancel_shared_refresh_or_mutate_request(self):
        client = self.client()
        started, release, canceled = (
            threading.Event(),
            threading.Event(),
            threading.Event(),
        )
        calls = []

        def network(request, timeout):
            calls.append((request.full_url, request.data, dict(request.header_items())))
            if request.full_url.endswith("/oauth2/token"):
                started.set()
                self.assertTrue(release.wait(2))
                return FakeResponse(
                    body=b'{"access_token":"fixture-token","token_type":"DPoP","expires_in":300,"scope":"platform.domains.read"}'
                )
            return FakeResponse(204)

        client._send = network
        errors = []

        def first():
            try:
                client.request("https://api.d0.eu/platform/v1/x", cancel=canceled)
            except Exception as error:  # noqa: BLE001 - collect failures across test threads
                errors.append(error)

        thread = threading.Thread(target=first)
        thread.start()
        self.assertTrue(started.wait(2))
        body = bytearray(b"original")
        headers = {"Idempotency-Key": "original-key"}
        result = []
        snapshotted = threading.Event()
        original_access_token = client._access_token

        def access_token(cancel, deadline):
            snapshotted.set()
            return original_access_token(cancel, deadline)

        client._access_token = access_token

        def second():
            result.append(
                client.request(
                    "https://api.d0.eu/platform/v1/x",
                    method="POST",
                    headers=headers,
                    body=body,
                )
            )

        other = threading.Thread(target=second)
        other.start()
        self.assertTrue(snapshotted.wait(2))
        body[:] = b"changed!"
        headers["Idempotency-Key"] = "changed-key"
        canceled.set()
        thread.join(2)
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], TimeoutError)
        release.set()
        other.join(2)
        self.assertEqual(result[0].status, 204)
        self.assertEqual(
            len([url for url, _, _ in calls if url.endswith("/oauth2/token")]), 1
        )
        self.assertEqual(calls[-1][1], b"original")
        self.assertEqual(calls[-1][2]["Idempotency-key"], "original-key")

    def test_redirect_business_status_and_nonce_bounds(self):
        for status in (307, 401, 429):
            client = self.client()
            client._token, client._expires = "fixture-token", time.monotonic() + 300
            calls = []

            def network(request, timeout, status=status, calls=calls):
                calls.append(request)
                return FakeResponse(
                    status, headers={"Location": "https://other.invalid/x"}
                )

            client._send = network
            if status == 307:
                with self.assertRaisesRegex(ValueError, "redirects"):
                    client.request("https://api.d0.eu/platform/v1/x")
            else:
                self.assertEqual(
                    client.request("https://api.d0.eu/platform/v1/x").status, status
                )
            self.assertEqual(len(calls), 1)

        client = self.client()
        token_calls = []

        def nonce_loop(request, timeout):
            token_calls.append(request)
            return FakeResponse(
                400, b'{"error":"use_dpop_nonce"}', {"DPoP-Nonce": "nonce"}
            )

        client._send = nonce_loop
        with self.assertRaises(ValueError):
            client.request("https://api.d0.eu/platform/v1/x")
        self.assertEqual(len(token_calls), 2)

    def test_rejects_oversized_token_and_sanitizes_transport_failure(self):
        client = self.client()
        client._send = lambda *_: FakeResponse(body=b"x" * 32769)
        with self.assertRaisesRegex(ValueError, "size"):
            client.request("https://api.d0.eu/platform/v1/x")
        client = self.client()
        client._send = lambda *_: (_ for _ in ()).throw(OSError("secret-token-body"))
        with self.assertRaises(RuntimeError) as caught:
            client.request("https://api.d0.eu/platform/v1/x")
        self.assertNotIn("secret-token-body", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
