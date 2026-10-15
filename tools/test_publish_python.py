import hashlib
import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

import publish_python


class PublishPythonTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "dist/python").mkdir(parents=True)
        self.archives = []
        self.versions = {"auth": "0.1.0", "eric": "0.1.1"}
        for product, version in self.versions.items():
            module = "d0_auth_machine" if product == "auth" else f"d0_{product}"
            for suffix in ("-py3-none-any.whl", ".tar.gz"):
                archive = self.root / f"dist/python/{module}-{version}{suffix}"
                archive.write_bytes(b"qualified fixture")
                self.archives.append(archive)
        self.env = {"GITHUB_REPOSITORY": "dev-null-GmbH/d0-sdk", "GITHUB_REF": "refs/heads/main", "ACTIONS_ID_TOKEN_REQUEST_URL": "https://oidc.invalid"}

    def test_outside_release_context_is_denied(self):
        with patch.dict("os.environ", {}, clear=True), patch.object(publish_python.subprocess, "run") as publish:
            with self.assertRaisesRegex(SystemExit, "OIDC"):
                publish_python.main()
            publish.assert_not_called()

    def test_partial_publication_resumes_only_identical_versions(self):
        existing = {"filename": self.archives[0].name, "digests": {"sha256": hashlib.sha256(b"qualified fixture").hexdigest()}}
        missing = urllib.error.HTTPError("https://pypi.org", 404, "missing", {}, None)
        with patch.dict("os.environ", self.env, clear=True), patch.object(publish_python, "ROOT", self.root), patch.object(publish_python, "versions", return_value=self.versions), patch("publish_python.urllib.request.urlopen", side_effect=[io.BytesIO(json.dumps({"urls": [existing]}).encode()), missing]), patch.object(publish_python.subprocess, "run") as publish:
            publish_python.main()
            self.assertEqual(publish.call_count, 3)
            self.assertEqual(publish.call_args_list[0].args[0][-1], str(self.archives[1]))
            self.assertTrue(all("always" in call.args[0] for call in publish.call_args_list))

    def test_late_collision_blocks_all_publication(self):
        missing = urllib.error.HTTPError("https://pypi.org", 404, "missing", {}, None)
        existing = {"filename": self.archives[2].name, "digests": {"sha256": "different bytes"}}
        with patch.dict("os.environ", self.env, clear=True), patch.object(publish_python, "ROOT", self.root), patch.object(publish_python, "versions", return_value=self.versions), patch("publish_python.urllib.request.urlopen", side_effect=[missing, io.BytesIO(json.dumps({"urls": [existing]}).encode())]), patch.object(publish_python.subprocess, "run") as publish:
            with self.assertRaisesRegex(SystemExit, "collision"):
                publish_python.main()
            publish.assert_not_called()

    def test_unreviewed_platform_wheel_blocks_publication(self):
        existing = {"filename": "d0_auth_machine-0.1.0-cp314-cp314-manylinux_2_28_x86_64.whl", "digests": {"sha256": "unreviewed"}}
        with patch.dict("os.environ", self.env, clear=True), patch.object(publish_python, "ROOT", self.root), patch.object(publish_python, "versions", return_value=self.versions), patch("publish_python.urllib.request.urlopen", return_value=io.BytesIO(json.dumps({"urls": [existing]}).encode())), patch.object(publish_python.subprocess, "run") as publish:
            with self.assertRaisesRegex(SystemExit, "unreviewed files"):
                publish_python.main()
            publish.assert_not_called()


if __name__ == "__main__":
    unittest.main()
