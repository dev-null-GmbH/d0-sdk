"""Offline production notice and accepted/rejected test simulation examples."""
import io
import json
from email.message import Message
from typing import Any

from d0_auth_machine import MachineClient

from d0_eric import EricClient, resource_for

TENANT = "11111111-1111-4111-8111-111111111111"
PRODUCT = "22222222-2222-4222-8222-222222222222"

class Response(io.BytesIO):
    def __init__(self, code: int, value: dict[str, Any]):
        super().__init__(json.dumps(value).encode())
        self.status = code
        self.headers = Message()
        self.headers["Content-Type"] = "application/json"

class FixtureMachine(MachineClient):
    def __init__(self, profile: str):
        self.resource = resource_for(profile)  # type: ignore[arg-type]

    def request(self, url: str, *, method: str = "GET", headers: Any = None, body: Any = None, cancel: Any = None, timeout: float = 45.0) -> Any:
        assert headers["X-ERIC-Tenant"] == TENANT
        if url.endswith("/notices"):
            return Response(200, {"schema_version": "eric.user-notices.v1", "version": "fixture", "sdk_release": "fixture", "documentation_archive_sha256": "0"*64, "license_document_sha256": "0"*64, "license_member": "license", "notices": []})
        if url.endswith("/simulations"):
            fixture = json.loads(body)["fixture"]
            return Response(202, {"id": "33333333-3333-4333-8333-333333333333", "fixture": fixture, "status": "completed", "outcome": "simulated_accepted" if fixture == "validation-accepted-v1" else "simulated_rejected", "simulated": True})
        raise AssertionError(url)

prod = EricClient("production", TENANT, FixtureMachine("production"))  # type: ignore[arg-type]
assert prod.get_user_notices({"productId": PRODUCT})["schema_version"] == "eric.user-notices.v1"
test = EricClient("test", TENANT, FixtureMachine("test"))  # type: ignore[arg-type]
for fixture, outcome in (("validation-accepted-v1", "simulated_accepted"), ("validation-rejected-v1", "simulated_rejected")):
    result = test.create_eric_test_simulation({"productId": PRODUCT, "idempotencyKey": "offline-eric-001", "body": {"fixture": fixture}})  # type: ignore[typeddict-item]
    assert result["outcome"] == outcome
print("ERiC production read-only + both test simulations: offline fixtures passed")
