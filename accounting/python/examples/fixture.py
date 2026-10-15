"""Standalone offline balanced draft example; never sends a network request."""
import io
import json
from email.message import Message
from typing import Any

from d0_auth_machine import MachineClient

from d0_accounting import AccountingClient, resource_for

SUFFIX = "9GXQ8W5V4R3P2N1M0KJHGF7ED6"
TENANT = "ten_" + SUFFIX


class Response(io.BytesIO):
    def __init__(self, status: int, body: dict[str, Any]):
        super().__init__(json.dumps(body).encode())
        self.status = status
        self.headers = Message()
        self.headers["Content-Type"] = "application/json"
        self.headers["ETag"] = '"fixture-v1"'


class FakeMachine(MachineClient):
    def __init__(self, profile: str):
        self.resource = resource_for(profile)  # type: ignore[arg-type]

    def request(self, url: str, *, method: str = "GET", headers: Any = None, body: Any = None, cancel: Any = None, timeout: float = 45.0) -> Any:
        assert url.startswith(self.resource + "/v1/")
        headers = dict(headers or {})
        assert headers["X-Accounting-Tenant"] == TENANT
        payload = json.loads(body) if body else {}
        if url.endswith("/accounts") and method == "POST":
            return Response(201, {"id": "acct_" + SUFFIX[:-1] + ("6" if payload["accountNo"] == "1200" else "7"), "accountNo": payload["accountNo"], "name": payload["name"], "createdAt": "2026-01-01T00:00:00Z"})
        if url.endswith("/periods") and method == "POST":
            return Response(201, {"id": "per_" + SUFFIX, **payload, "status": "open", "createdAt": "2026-01-01T00:00:00Z"})
        if url.endswith("/journal-entries") and method == "POST":
            lines = payload["lines"]
            assert [line["amount"]["amount"] for line in lines] == ["150000", "150000"]
            assert [line["side"] for line in lines] == ["debit", "credit"]
            return Response(201, {"id": "je_" + SUFFIX, "status": "draft", **payload, "createdAt": "2026-01-01T00:00:00Z"})
        raise AssertionError("unexpected fixture route")


for profile in ("production", "test"):
    client = AccountingClient(profile, TENANT, FakeMachine(profile))  # type: ignore[arg-type]
    debit = client.create_account({"idempotencyKey": "fixture-account-00001", "body": {"accountNo": "1200", "name": "Bank"}})
    credit = client.create_account({"idempotencyKey": "fixture-account-00002", "body": {"accountNo": "4000", "name": "Revenue"}})
    period = client.create_period({"idempotencyKey": "fixture-period-00001", "body": {"label": "2026-01", "startsOn": "2026-01-01", "endsOn": "2026-01-31"}})
    draft = client.create_journal_entry_draft({"idempotencyKey": "fixture-draft-000001", "body": {"periodId": period["id"], "bookingDate": "2026-01-15", "currency": "EUR", "lines": [
        {"accountId": debit["id"], "side": "debit", "amount": {"amount": "150000", "currency": "EUR"}},
        {"accountId": credit["id"], "side": "credit", "amount": {"amount": "150000", "currency": "EUR"}},
    ]}})
    assert draft["id"] == "je_" + SUFFIX and draft["status"] == "draft"
    print(f"{profile}: balanced unposted draft {draft['id']}")
