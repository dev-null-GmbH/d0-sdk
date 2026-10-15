import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

import publish_npm


class PublishTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "dist/npm").mkdir(parents=True)
        for name in ("auth-machine", "platform", "accounting", "einvoice", "eric"):
            version = "0.1.1" if name == "eric" else "0.1.0"
            (self.root / f"dist/npm/dev-null-gmbh-{name}-{version}.tgz").write_bytes(b"qualified fixture")
        for product in ("auth", "platform", "accounting", "einvoice", "eric"):
            base = self.root / product
            (base / "typescript").mkdir(parents=True)
            (base / "python").mkdir()
            version = "0.1.1" if product == "eric" else "0.1.0"
            (base / "typescript/package.json").write_text(json.dumps({"version": version}))
            (base / "python/pyproject.toml").write_text(f'[project]\nversion = "{version}"\n')
        self.environment = {"GITHUB_REPOSITORY": "dev-null-GmbH/d0-sdk", "GITHUB_REF": "refs/heads/main", "ACTIONS_ID_TOKEN_REQUEST_URL": "https://oidc.invalid"}

    def test_never_publishes_outside_release_context(self):
        with patch.dict("os.environ", {}, clear=True), patch("publish_npm.subprocess.run") as publish:
            with self.assertRaisesRegex(SystemExit, "OIDC"):
                publish_npm.main()
            publish.assert_not_called()

    def test_collision_preflight_blocks_all_publication(self):
        metadata = io.BytesIO(json.dumps({"dist": {"integrity": "different bytes"}}).encode())
        with patch.dict("os.environ", self.environment, clear=True), patch.object(publish_npm, "ROOT", self.root), patch("publish_npm.urllib.request.urlopen", return_value=metadata), patch("publish_npm.subprocess.run") as publish:
            with self.assertRaisesRegex(SystemExit, "collision"):
                publish_npm.main()
            publish.assert_not_called()

    def test_new_packages_publish_auth_first_without_lifecycle_scripts(self):
        missing = urllib.error.HTTPError("https://registry.npmjs.org", 404, "missing", {}, None)
        with patch.dict("os.environ", self.environment, clear=True), patch.object(publish_npm, "ROOT", self.root), patch("publish_npm.urllib.request.urlopen", side_effect=missing), patch("publish_npm.subprocess.run") as publish:
            publish_npm.main()
            self.assertEqual(publish.call_count, 5)
            self.assertIn("auth-machine", publish.call_args_list[0].args[0][2])
            self.assertTrue(publish.call_args_list[-1].args[0][2].endswith("eric-0.1.1.tgz"))
            self.assertTrue(all("--ignore-scripts" in call.args[0] for call in publish.call_args_list))


if __name__ == "__main__":
    unittest.main()
