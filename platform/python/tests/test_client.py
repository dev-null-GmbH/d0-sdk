import io
import json
import threading
import unittest
import urllib.parse
from collections import Counter
from email.message import Message
from typing import Any

from d0_auth_machine import MachineClient

from d0_platform import (
    APIError,
    PlatformClient,
    resource_for,
    wait_for,
    walk_audit_events,
)
from d0_platform.methods import PlatformOperations
from d0_platform.operations import OPERATIONS


class Response(io.BytesIO):
    def __init__(self, status: int, body: dict[str, Any] | None):
        super().__init__(json.dumps(body).encode() if body is not None else b"")
        self.status = status
        self.headers = Message()
        self.headers["Content-Type"] = "application/json"
        self.headers["ETag"] = '"fixture-v1"'
        self.headers["X-Request-ID"] = "fixture-request"


class FakeMachine(MachineClient):
    def __init__(self, profile: str):
        self.resource = resource_for(profile)  # type: ignore[arg-type]
        self.calls: list[tuple[str, str, bytes | None]] = []

    def request(self, url: str, *, method: str = "GET", headers: Any = None, body: Any = None, cancel: Any = None, timeout: float = 45.0) -> Any:
        assert url.startswith(self.resource + "/v1/")
        self.calls.append((url, method, body))
        if url.endswith("/domains") and method == "GET":
            return Response(200, {"domains": [{"fqdn": "example.eu", "status": "active", "created_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-01T00:00:00Z"}]})
        if url.endswith("/dns/records/www/A") and method == "PUT":
            return Response(200, {"name": "www.example.eu", "type": "A", "ttl": 300, "records": ["192.0.2.1"], "read_only": False})
        if url.endswith("/dns/records") and method == "GET":
            return Response(200, {"records": [{"name": "www.example.eu", "type": "A", "ttl": 300, "records": ["192.0.2.1"], "read_only": False}]})
        if url.endswith("/dns/records/www/A") and method == "DELETE":
            return Response(204, None)
        if url.endswith("/object-storage/buckets/bucket_fixture") and method == "DELETE":
            return Response(202, None)
        if "/audit/events" in url and method == "GET":
            before = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query).get("before", [""])[0]
            return Response(200, {"events": [], "next_before": "older" if not before else ""})
        raise AssertionError("unexpected fixture route")


class SDKTests(unittest.TestCase):
    def test_contract_coverage(self) -> None:
        self.assertEqual(len(OPERATIONS), 30)
        self.assertEqual(Counter(op["test"] for op in OPERATIONS.values()), {False: 25, True: 5})
        public_methods = {name for name, value in vars(PlatformOperations).items() if not name.startswith("_") and callable(value)}
        self.assertEqual(len(public_methods), 30)

    def test_dns_both_profiles(self) -> None:
        for profile in ("production", "test"):
            with self.subTest(profile=profile):
                transport = FakeMachine(profile)
                sdk = PlatformClient(profile, transport)  # type: ignore[arg-type]
                domain = sdk.list_domains({})["domains"][0]["fqdn"]
                result = sdk.upsert_dns_record({"domain": domain, "name": "www", "type": "A", "body": {"records": ["192.0.2.1"], "ttl": 300}})
                self.assertEqual(result["name"], "www.example.eu")
                listing = sdk.call_with_response("listDNSRecords", {"domain": domain})
                self.assertEqual(listing["etag"], '"fixture-v1"')
                self.assertEqual(listing["request_id"], "fixture-request")
                sdk.delete_dns_record({"domain": domain, "name": "www", "type": "A"})
                self.assertEqual(len(transport.calls), 4)
                if profile == "test":
                    with self.assertRaisesRegex(ValueError, "unavailable"):
                        sdk.get_cluster_catalog({})
                    self.assertEqual(len(transport.calls), 4)

    def test_crossovers_and_errors(self) -> None:
        transport = FakeMachine("test")
        with self.assertRaisesRegex(ValueError, "resource"):
            PlatformClient("production", transport)
        sdk = PlatformClient("test", transport)
        with self.assertRaisesRegex(ValueError, "identifier"):
            sdk.get_domain({"domain": "../secret"})
        self.assertEqual(transport.calls, [])
        self.assertNotIn("raw secret", str(APIError(409)))

    def test_key_empty_202_audit_cursor_and_cancel(self) -> None:
        transport = FakeMachine("production")
        sdk = PlatformClient("production", transport)
        with self.assertRaisesRegex(ValueError, "idempotency"):
            sdk.delete_cluster({"id": "cl_fixture", "idempotencyKey": "short"})
        self.assertEqual(transport.calls, [])
        with self.assertRaisesRegex(ValueError, "required"):
            sdk.delete_cluster({"id": "cl_fixture"})  # type: ignore[typeddict-item]
        self.assertEqual(transport.calls, [])
        self.assertIsNone(sdk.delete_object_storage_bucket({"id": "bucket_fixture"}))
        pages: list[Any] = []
        self.assertEqual(walk_audit_events(sdk, pages.append, limit=2, max_pages=3), "")
        self.assertEqual(len(pages), 2)
        self.assertNotIn("before=", transport.calls[1][0])
        self.assertIn("before=older", transport.calls[2][0])
        cancel = threading.Event()
        cancel.set()
        with self.assertRaises(TimeoutError):
            wait_for(lambda _: 0, lambda n: n == 1, 1, cancel)

    def test_problem_discards_raw_detail(self) -> None:
        class ErrorMachine(FakeMachine):
            def request(self, url: str, *, method: str = "GET", headers: Any = None, body: Any = None, cancel: Any = None, timeout: float = 45.0) -> Any:
                response = Response(409, {"type": "conflict", "title": "Conflict", "detail": "raw secret"})
                response.headers.replace_header("Content-Type", "application/problem+json")
                return response

        sdk = PlatformClient("production", ErrorMachine("production"))
        with self.assertRaises(APIError) as failure:
            sdk.list_domains({})
        self.assertEqual(failure.exception.request_id, "fixture-request")
        self.assertNotIn("raw secret", str(failure.exception))


if __name__ == "__main__":
    unittest.main()
