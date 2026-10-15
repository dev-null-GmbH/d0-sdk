import io
import json
import unittest
from collections import Counter
from email.message import Message
from typing import Any

from d0_auth_machine import MachineClient

from d0_accounting import AccountingClient, resource_for
from d0_accounting.methods import AccountingOperations
from d0_accounting.operations import OPERATIONS

SUFFIX = "9GXQ8W5V4R3P2N1M0KJHGF7ED6"
TENANT = "ten_" + SUFFIX
KEY = "fixture-key-00000001"


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
        self.calls: list[tuple[str, str, dict[str, str], bytes | None]] = []

    def request(self, url: str, *, method: str = "GET", headers: Any = None, body: Any = None, cancel: Any = None, timeout: float = 45.0) -> Any:
        assert url.startswith(self.resource + "/v1/")
        headers = dict(headers or {})
        self.calls.append((url, method, headers, body))
        payload = json.loads(body) if body else {}
        if url.endswith("/accounts") and method == "POST":
            return Response(201, {"id": "acct_" + SUFFIX, "accountNo": payload["accountNo"], "name": payload["name"], "createdAt": "2026-01-01T00:00:00Z"})
        if url.endswith("/periods") and method == "POST":
            return Response(201, {"id": "per_" + SUFFIX, **payload, "status": "open", "createdAt": "2026-01-01T00:00:00Z"})
        if url.endswith("/journal-entries") and method == "POST":
            lines = payload["lines"]
            assert [line["amount"]["amount"] for line in lines] == ["150000", "150000"]
            assert [line["side"] for line in lines] == ["debit", "credit"]
            return Response(201, {"id": "je_" + SUFFIX, "status": "draft", **payload, "createdAt": "2026-01-01T00:00:00Z"})
        raise AssertionError("unexpected fixture route")


class SDKTests(unittest.TestCase):
    def test_catalog_coverage(self) -> None:
        self.assertEqual(len(OPERATIONS), 56)
        self.assertEqual(Counter(op["test"] for op in OPERATIONS.values()), {False: 44, True: 12})
        public_methods = {name for name, value in vars(AccountingOperations).items() if not name.startswith("_") and callable(value)}
        self.assertEqual(len(public_methods), 56)
        self.assertIn("create_zugferd_pdf", public_methods)

    def test_balanced_draft_both_profiles(self) -> None:
        for profile in ("production", "test"):
            with self.subTest(profile=profile):
                transport = FakeMachine(profile)
                sdk = AccountingClient(profile, TENANT, transport)  # type: ignore[arg-type]
                debit = sdk.create_account({"idempotencyKey": KEY, "body": {"accountNo": "1200", "name": "Bank"}})
                credit = sdk.create_account({"idempotencyKey": "fixture-key-00000002", "body": {"accountNo": "4000", "name": "Revenue"}})
                period = sdk.create_period({"idempotencyKey": "fixture-key-00000003", "body": {"label": "2026-01", "startsOn": "2026-01-01", "endsOn": "2026-01-31"}})
                draft = sdk.create_journal_entry_draft({"idempotencyKey": "fixture-key-00000004", "body": {"periodId": period["id"], "bookingDate": "2026-01-15", "currency": "EUR", "lines": [
                    {"accountId": debit["id"], "side": "debit", "amount": {"amount": "150000", "currency": "EUR"}},
                    {"accountId": credit["id"], "side": "credit", "amount": {"amount": "150000", "currency": "EUR"}},
                ]}})
                self.assertEqual(draft["status"], "draft")
                self.assertEqual(sdk.last_response["etag"], '"fixture-v1"')
                response = sdk.call_with_response("createAccount", {"idempotencyKey": "fixture-key-00000006", "body": {"accountNo": "1000", "name": "Cash"}})
                self.assertEqual(response["etag"], '"fixture-v1"')
                self.assertEqual(len(transport.calls), 5)
                self.assertTrue(all(headers["X-Accounting-Tenant"] == TENANT for _, _, headers, _ in transport.calls))
                if profile == "test":
                    with self.assertRaisesRegex(ValueError, "unavailable"):
                        sdk.post_journal_entry({"entryId": draft["id"], "idempotencyKey": "fixture-key-00000005"})
                    self.assertEqual(len(transport.calls), 5)

    def test_rejects_invalid_key_and_tenant(self) -> None:
        transport = FakeMachine("test")
        with self.assertRaisesRegex(ValueError, "tenant"):
            AccountingClient("test", "raw-tenant", transport)
        sdk = AccountingClient("test", TENANT, transport)
        with self.assertRaisesRegex(ValueError, "idempotency"):
            sdk.create_account({"idempotencyKey": "short", "body": {"accountNo": "1200", "name": "Bank"}})
        with self.assertRaisesRegex(ValueError, "decimal strings"):
            sdk.create_journal_entry_draft({"idempotencyKey": KEY, "body": {"periodId": "per_" + SUFFIX, "bookingDate": "2026-01-15", "currency": "EUR", "lines": [
                {"accountId": "acct_" + SUFFIX, "side": "debit", "amount": {"amount": 150000, "currency": "EUR"}},
                {"accountId": "acct_" + SUFFIX, "side": "credit", "amount": {"amount": "150000", "currency": "EUR"}},
            ]}})
        self.assertEqual(transport.calls, [])


if __name__ == "__main__":
    unittest.main()
