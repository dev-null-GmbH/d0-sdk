import json
import unittest

from import_sources import exported, transform
from verify_export import verify_inventory


class ExportTests(unittest.TestCase):
    def test_public_inventory_rejects_unmanifested_files_and_omissions(self):
        expected = {"go.work", "auth/go/client.go"}
        verify_inventory(expected, expected)
        for extra in ["auth/go/private.env", "auth/go/unreviewed.go", "internal/private-service.go"]:
            with self.assertRaises(AssertionError):
                verify_inventory(expected | {extra}, expected)
        with self.assertRaises(AssertionError):
            verify_inventory({"go.work"}, expected)

    def test_closed_source_surface(self):
        for path in ["go/client.go", "python/src/d0_platform/py.typed", "typescript/src/index.ts", "contracts/test/public-openapi.json"]:
            self.assertTrue(exported(path))
        for path in ["cmd/server/main.go", "internal/accounts/token.go", "db/migrations/001.sql", ".env", "python/uv.lock", "typescript/package-lock.json"]:
            self.assertFalse(exported(path))
        for path in ["../internal/secret", "/absolute/path", "go/../../secret"]:
            with self.assertRaises(ValueError):
                exported(path)

    def test_public_dependencies_and_unknown_override_fail_closed(self):
        raw = json.dumps({"private": True, "dependencies": {"@dev-null-gmbh/auth-machine": "file:../../../d0-auth/packages/machine/typescript"}}).encode()
        package = json.loads(transform("platform", "typescript/package.json", raw))
        self.assertNotIn("private", package)
        self.assertEqual(package["dependencies"]["@dev-null-gmbh/auth-machine"], "0.1.0")
        self.assertEqual(package["publishConfig"]["registry"], "https://registry.npmjs.org")
        with self.assertRaises(ValueError):
            transform("platform", "go/go.mod", b"module x\nreplace arbitrary => ../private\n")
        with self.assertRaises(ValueError):
            transform("platform", "python/pyproject.toml", b'unknown = "../../../private"')


if __name__ == "__main__":
    unittest.main()
