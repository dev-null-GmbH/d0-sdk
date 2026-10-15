import base64
import hashlib
import io
import json
import threading
import unittest

from d0_auth_machine import MachineClient

from d0_einvoice import APIError, EInvoiceClient, resource_for

DOC = "doc_abcdefghijklmnopqrst"
OP = "vop_abcdefghijklmnopqrst"
POLICY = "vpol_abcdefghijklmnopqrst"
KEY = "fixture-key-00000001"


class Response:
    def __init__(self, status, body, media="application/json", request_id=""):
        self.status = status
        self.headers = {"Content-Type": media, "X-Request-ID": request_id}
        self.stream = io.BytesIO(json.dumps(body).encode())
        self.closed = False

    def read(self, length):
        return self.stream.read(length)

    def close(self):
        self.closed = True


class FixtureMachine(MachineClient):
    def __init__(self, profile):
        self.resource = resource_for(profile)
        self.calls = []
        self.last_response = None

    def request(self, url, **options):
        assert url.startswith(self.resource + "/v1/")
        self.calls.append((url, options))
        path = url.removeprefix(self.resource + "/v1")
        if path == "/documents":
            body = options["body"]
            digest = "sha-256=:" + base64.b64encode(hashlib.sha256(body).digest()).decode() + ":"
            assert options["headers"]["Content-Digest"] == digest
            assert options["headers"]["Idempotency-Key"] == KEY
            response = Response(201, {"id": DOC})
        elif path == "/documents/" + DOC:
            response = Response(200, {"id": DOC})
        elif path == "/validation-operations":
            assert json.loads(options["body"]) == {"documentId": DOC, "validationPolicyId": POLICY}
            assert options["headers"]["Idempotency-Key"] == KEY
            response = Response(202, {"id": OP, "status": "queued"})
        elif path == "/validation-operations/" + OP:
            response = Response(200, {"id": OP, "status": "succeeded"})
        elif path == "/validation-operations/" + OP + "/result":
            response = Response(200, {"operationId": OP, "valid": False, "issues": [{"code": "fixture.invalid"}]})
        elif path.startswith("/validation-policies?"):
            assert "cursor=opaque%2Bcursor" in path
            response = Response(200, {"items": [{"id": POLICY}]})
        elif path == "/validation-policies/" + POLICY:
            response = Response(200, {"id": POLICY})
        else:
            raise AssertionError(path)
        self.last_response = response
        return response


class ClientTest(unittest.TestCase):
    def test_all_seven_operations_both_profiles(self):
        for profile in ("production", "test"):
            with self.subTest(profile=profile):
                transport = FixtureMachine(profile)
                client = EInvoiceClient(profile, transport)
                self.assertEqual(client.create_document(b"<synthetic/>", KEY)["id"], DOC)
                self.assertTrue(transport.last_response.closed)
                self.assertEqual(client.get_document(DOC)["id"], DOC)
                self.assertEqual(client.create_validation_operation(DOC, POLICY, KEY)["id"], OP)
                self.assertEqual(client.get_validation_operation(OP)["status"], "succeeded")
                self.assertFalse(client.get_validation_result(OP)["valid"])
                self.assertEqual(client.list_validation_policies(7, "opaque+cursor")["items"][0]["id"], POLICY)
                self.assertEqual(client.get_validation_policy(POLICY)["id"], POLICY)
                self.assertEqual(len(transport.calls), 7)

    def test_profile_ids_errors_and_poll_cancellation(self):
        with self.assertRaises(ValueError):
            EInvoiceClient("production", FixtureMachine("test"))
        transport = FixtureMachine("test")
        client = EInvoiceClient("test", transport)
        with self.assertRaises(ValueError):
            client.get_document("doc_../x")
        with self.assertRaises(ValueError):
            client.create_document(b"<synthetic/>", "short")
        cancelled = threading.Event()
        cancelled.set()
        with self.assertRaises(TimeoutError):
            client.wait_validation(OP, 2, cancel=cancelled)
        self.assertEqual(transport.calls, [])
        def queued(url, **options):
            return Response(200, {"id": OP, "status": "queued"})
        transport.request = queued
        with self.assertRaises(TimeoutError):
            client.wait_validation(OP, 0.005)
        def queued_with_hint(url, **options):
            response = Response(200, {"id": OP, "status": "queued"})
            response.headers["Retry-After"] = "3"
            return response
        transport.request = queued_with_hint
        hint = []
        client._get_validation_operation(OP, retry=hint)
        self.assertEqual(hint, [3.0])
        def failure(url, **options):
            return Response(409, {"status": 409, "type": "https://api.d0.eu/einvoice/problems/result-not-ready",
                                  "title": "Not ready", "detail": "SECRET XML"}, "application/problem+json", "request-123")
        transport.request = failure
        with self.assertRaises(APIError) as raised:
            client.get_validation_result(OP)
        self.assertEqual(raised.exception.request_id, "request-123")
        self.assertNotIn("SECRET", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
