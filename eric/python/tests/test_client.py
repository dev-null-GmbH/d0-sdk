import base64
import hashlib
import io
import json
import unittest
from collections import Counter
from email.message import Message
from typing import Any

from d0_auth_machine import MachineClient

from d0_eric import APIError, EricClient, resource_for, wait_for
from d0_eric.methods import EricOperations
from d0_eric.operations import OPERATIONS

TENANT = "11111111-1111-4111-8111-111111111111"
PRODUCT = "22222222-2222-4222-8222-222222222222"
SIMULATION = "33333333-3333-4333-8333-333333333333"
KEY = "fixture-eric-001"

class Response(io.BytesIO):
    def __init__(self, status: int, body: bytes, content_type: str, extra: dict[str, str] | None = None):
        super().__init__(body)
        self.status = status
        self.headers = Message()
        self.headers["Content-Type"] = content_type
        for k, v in (extra or {}).items():
            self.headers[k] = v

class FakeMachine(MachineClient):
    def __init__(self, profile: str):
        self.profile = profile
        self.resource = resource_for(profile)  # type: ignore[arg-type]
        self.calls: list[tuple[str,str,dict[str,str]]] = []
        self.tamper = False

    def request(self, url: str, *, method: str = "GET", headers: Any = None, body: Any = None, cancel: Any = None, timeout: float = 45.0) -> Any:
        h = dict(headers or {})
        self.calls.append((url,method,h))
        assert h["X-ERIC-Tenant"] == TENANT
        if self.profile == "test":
            assert url.startswith(self.resource + f"/v1/tenants/{TENANT}/products/{PRODUCT}/simulations")
            fixture = json.loads(body)["fixture"] if body else "validation-accepted-v1"
            payload = {"id": SIMULATION, "fixture": fixture, "status": "completed", "outcome": "simulated_accepted" if fixture == "validation-accepted-v1" else "simulated_rejected", "simulated": True}
            return Response(202 if method == "POST" else 200, json.dumps(payload).encode(), "application/json")
        assert url.startswith(self.resource + f"/v1/products/{PRODUCT}/")
        if url.endswith("/notices"):
            payload = {"schema_version": "eric.user-notices.v1", "version": "fixture", "sdk_release": "fixture", "documentation_archive_sha256": "0"*64, "license_document_sha256": "0"*64, "license_member": "license", "notices": []}
            return Response(200, json.dumps(payload).encode(), "application/json")
        if url.endswith("/payload.xml"):
            data = b"<fixture/>"
            digest = "sha-256=:" + base64.b64encode(hashlib.sha256(data).digest()).decode() + ":"
            return Response(200, data if not self.tamper else b"<bad/>", "application/xml", {"Content-Digest": digest})
        if url.endswith("/content"):
            data = bytes((0, 1, 255))
            digest = "sha-256=:" + base64.b64encode(hashlib.sha256(data).digest()).decode() + ":"
            return Response(200, data, "application/octet-stream", {"Content-Digest": digest, "Content-Length": "4" if self.tamper else "3"})
        raise AssertionError(url)

class SDKTests(unittest.TestCase):
    def test_catalog_coverage(self) -> None:
        self.assertEqual(len(OPERATIONS), 51)
        self.assertEqual(Counter(op["profile"] for op in OPERATIONS.values()), {"production": 49, "test": 2})
        public_methods = {k for k,v in vars(EricOperations).items() if not k.startswith("_") and callable(v)}
        self.assertEqual(len(public_methods), 51)

    def test_both_simulation_outcomes_and_gates(self) -> None:
        transport = FakeMachine("test")
        sdk = EricClient("test", TENANT, transport)  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError,"unavailable"):
            sdk.get_user_notices({"productId":PRODUCT})
        self.assertEqual(len(transport.calls),0)
        for fixture, outcome in (("validation-accepted-v1","simulated_accepted"),("validation-rejected-v1","simulated_rejected")):
            created = sdk.create_eric_test_simulation({"productId":PRODUCT,"idempotencyKey":KEY,"body":{"fixture":fixture}})  # type: ignore[typeddict-item]
            self.assertEqual(created["outcome"],outcome)
            self.assertTrue(sdk.get_eric_test_simulation({"productId":PRODUCT,"simulationId":created["id"]})["simulated"])
        self.assertEqual(len(transport.calls),4)
        with self.assertRaisesRegex(ValueError,"idempotency"):
            sdk.create_eric_test_simulation({"productId":PRODUCT,"idempotencyKey":"bad key","body":{"fixture":"validation-accepted-v1"}})
        with self.assertRaisesRegex(ValueError,"identifier"):
            sdk.get_eric_test_simulation({"productId":"raw","simulationId":SIMULATION})
        self.assertEqual(len(transport.calls),4)

    def test_production_read_and_digest(self) -> None:
        transport = FakeMachine("production")
        sdk = EricClient("production", TENANT, transport)  # type: ignore[arg-type]
        self.assertEqual(sdk.get_user_notices({"productId":PRODUCT})["schema_version"],"eric.user-notices.v1")
        artifact = sdk.get_preparation_artifact({"productId":PRODUCT,"preparationId":SIMULATION,"kind":"payload.xml"})
        self.assertEqual(artifact["bytes"],b"<fixture/>")
        binary = sdk.get_retrieval_artifact_content({"productId": PRODUCT, "artifactId": SIMULATION, "kind": "content", "xEricActorStatus": "fixture-jws"})
        self.assertEqual(binary["bytes"], bytes((0, 1, 255)))
        transport.tamper = True
        with self.assertRaisesRegex(ValueError,"Digest"):
            sdk.get_preparation_artifact({"productId":PRODUCT,"preparationId":SIMULATION,"kind":"payload.xml"})
        with self.assertRaisesRegex(ValueError,"Length"):
            sdk.get_retrieval_artifact_content({"productId": PRODUCT, "artifactId": SIMULATION, "kind": "content", "xEricActorStatus": "fixture-jws"})
        with self.assertRaisesRegex(ValueError,"unavailable"):
            sdk.create_eric_test_simulation({"productId":PRODUCT,"idempotencyKey":KEY,"body":{"fixture":"validation-accepted-v1"}})

    def test_errors_and_poll_bounds(self) -> None:
        with self.assertRaisesRegex(ValueError,"tenant"):
            EricClient("test","raw",FakeMachine("test"))  # type: ignore[arg-type]
        self.assertEqual(str(APIError(409)),"ERiC request failed (HTTP 409)")
        with self.assertRaisesRegex(ValueError,"timeout"):
            wait_for(lambda: 1,lambda _:True,0)
        self.assertEqual(wait_for(lambda: 7,lambda _:True,1),7)

if __name__ == "__main__":
    unittest.main()
