"""Offline production/test DNS example using the actual Platform client transport API."""
import io
import json
from email.message import Message
from typing import Any

from d0_auth_machine import MachineClient

from d0_platform import PlatformClient, resource_for


class FixtureTransport(MachineClient):
    def __init__(self, profile: str):
        self.resource = resource_for(profile)  # type: ignore[arg-type]

    def request(self, url: str, *, method: str = "GET", headers: Any = None, body: Any = None, cancel: Any = None, timeout: float = 45.0) -> Any:
        assert url.startswith(self.resource + "/v1/")
        if url.endswith("/domains") and method == "GET":
            data: dict[str, Any] = {"domains": [{"fqdn": "example.eu", "status": "active", "created_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-01T00:00:00Z"}]}
        elif url.endswith("/dns/records/www/A") and method == "PUT":
            data = {"name": "www.example.eu", "type": "A", "ttl": 300, "records": ["192.0.2.1"], "read_only": False}
        else:
            raise AssertionError("unexpected route")
        response = io.BytesIO(json.dumps(data).encode())
        response.status = 200  # type: ignore[attr-defined]
        response.headers = Message()  # type: ignore[attr-defined]
        response.headers["Content-Type"] = "application/json"  # type: ignore[attr-defined]
        return response


for profile in ("production", "test"):
    sdk = PlatformClient(profile, FixtureTransport(profile))  # type: ignore[arg-type]
    domain = sdk.list_domains({})["domains"][0]["fqdn"]
    record = sdk.upsert_dns_record({"domain": domain, "name": "www", "type": "A", "body": {"records": ["192.0.2.1"], "ttl": 300}})
    assert record["name"] == "www.example.eu"
    print(f"{profile}: {record['name']}")
