import io
import tempfile
import unittest
import zipfile
from pathlib import Path

from rescan_release import digest, verify_archive


def bundle(name="npm/package.tgz", extra=False):
    raw = io.BytesIO()
    with zipfile.ZipFile(raw, "w") as archive:
        package = b"fixture"
        archive.writestr(name, package)
        archive.writestr("SHA256SUMS", f"{digest(package)}  {name}\n")
        if extra:
            archive.writestr("unlisted.txt", "fixture")
    return raw.getvalue()


class ReleaseArchiveTest(unittest.TestCase):
    def test_archive_requires_exact_bytes_and_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            raw = bundle()
            verify_archive(raw, len(raw), digest(raw), path)
            self.assertEqual((path / "npm/package.tgz").read_bytes(), b"fixture")
            with self.assertRaisesRegex(ValueError, "pinned"):
                verify_archive(raw, len(raw), "0" * 64, path)
            for invalid in [bundle(extra=True), bundle(name="npm/../../outside")]:
                with self.assertRaises(ValueError):
                    verify_archive(invalid, len(invalid), digest(invalid), path)
