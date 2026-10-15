"""Run both fixed product profiles against a synthetic in-memory transport."""

import io
import json
from urllib.parse import urlsplit

from d0_auth_machine import MachineClient

from d0_einvoice import EInvoiceClient, resource_for

DOCUMENT = "doc_abcdefghijklmnopqrst"
OPERATION = "vop_abcdefghijklmnopqrst"
POLICY = "vpol_abcdefghijklmnopqrst"


class Response:
    def __init__(self, status, value):
        self.status = status
        self.headers = {"Content-Type": "application/json"}
        self.body = io.BytesIO(json.dumps(value).encode())

    def read(self, length):
        return self.body.read(length)

    def close(self):
        self.body.close()


class FixtureMachine(MachineClient):
    def __init__(self, profile):
        self.resource = resource_for(profile)

    def request(self, url, **options):
        if not url.startswith(self.resource + "/v1/"):
            raise ValueError("profile crossover")
        path = urlsplit(url).path
        if path == "/einvoice/v1/validation-policies":
            return Response(200, {"items": [{"id": POLICY}]})
        if path == "/einvoice/v1/documents":
            return Response(201, {"id": DOCUMENT})
        if path == "/einvoice/v1/validation-operations":
            return Response(202, {"id": OPERATION, "status": "queued"})
        if path == "/einvoice/v1/validation-operations/" + OPERATION:
            return Response(200, {"id": OPERATION, "status": "succeeded"})
        if path == "/einvoice/v1/validation-operations/" + OPERATION + "/result":
            return Response(200, {"operationId": OPERATION, "valid": False, "issues": [{"code": "fixture.invalid"}]})
        raise ValueError("unexpected fixture route")


for profile in ("production", "test"):
    client = EInvoiceClient(profile, FixtureMachine(profile))
    policies = client.list_validation_policies()
    document = client.create_document(b"<synthetic/>", "fixture-upload-00000001")
    operation = client.create_validation_operation(document["id"], policies["items"][0]["id"], "fixture-validate-00000001")
    terminal = client.wait_validation(operation["id"], 2)
    result = client.get_validation_result(terminal["id"])
    print(profile, "fixture: operation=", terminal["id"], "valid=", result["valid"])
