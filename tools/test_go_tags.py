import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import go_tags


class GoTagTests(unittest.TestCase):
    def test_existing_version_accepts_only_identical_complete_module_tree(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root, text=True).strip()
            git("init", "-q")
            git("config", "user.name", "SDK fixture")
            git("config", "user.email", "sdk@example.invalid")
            module = root / "auth/go"
            module.mkdir(parents=True)
            (module / "go.mod").write_text("module fixture.invalid/auth\n")
            git("add", ".")
            git("commit", "-qm", "initial module")
            original = git("rev-parse", "HEAD")
            (root / "README.md").write_text("unrelated release documentation\n")
            git("add", ".")
            git("commit", "-qm", "documentation only")
            with patch.object(go_tags, "ROOT", root):
                self.assertTrue(go_tags.matching_tree(original, "auth"))
                (module / "client.go").write_text("package auth\n")
                git("add", ".")
                git("commit", "-qm", "changed module")
                self.assertFalse(go_tags.matching_tree(original, "auth"))

    def test_conflict_prevents_creating_any_pending_tag(self):
        def git(*args):
            if args == ("rev-parse", "HEAD"):
                return "a" * 40
            if args[0] == "ls-remote":
                return "" if "/auth/" in args[-1] else "b" * 40 + "\t" + args[-1]
            return ""
        env = {"GITHUB_REPOSITORY": go_tags.REPOSITORY, "GITHUB_REF": "refs/heads/main", "RELEASE_SHA": "a" * 40}
        with patch("sys.argv", ["go_tags.py", "--publish"]), patch.dict("os.environ", env, clear=True), patch.object(go_tags, "git", side_effect=git), patch.object(go_tags, "versions", return_value={"auth": "0.1.0", "eric": "0.1.1"}), patch.object(go_tags, "matching_tree", return_value=False), patch.object(go_tags.subprocess, "run") as publish:
            with self.assertRaisesRegex(SystemExit, "collision"):
                go_tags.main()
            publish.assert_not_called()


if __name__ == "__main__":
    unittest.main()
