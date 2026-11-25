#!/usr/bin/env python3
"""Verify a supported public archive and repeat clean consumer installations."""

import argparse
import hashlib
import json
import re
import subprocess
import tarfile
import tempfile
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path, PurePosixPath

from check_install import qualify
from verify_export import ROOT, versions

RELEASES = {
    "sdk-2026-10-15": (
        "6f2c39612a661ec557e96e5caff093a057e6e1de", 404724,
        "6c11b63a5ce5f24dff79d1f3d33c7879ff48831d66dd9029b37abf073152dd93",
    ),
    "sdk-2026-10-27": (
        "41cc1bbd8f2823a4f0d97bde76b91184dfab1aad", 429529,
        "e5647b2949898c36f71ebf4b7c12ad1a8d3a8a503603b605cb4f83ea06e9101f",
    ),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_archive(raw, size, sha256, directory):
    if len(raw) != size or digest(raw) != sha256:
        raise ValueError("public release ZIP differs from its pinned size or digest")
    with zipfile.ZipFile(BytesIO(raw)) as bundle:
        checksums = {}
        for line in bundle.read("SHA256SUMS").decode("ascii").splitlines():
            sha, name = line.split("  ", 1)
            path = PurePosixPath(name)
            if (not re.fullmatch(r"[0-9a-f]{64}", sha) or not path.parts or name in checksums or
                path.is_absolute() or ".." in path.parts or "\\" in name or
                path.parts[0] not in {"go", "npm", "python"} or name != path.as_posix()):
                raise ValueError(f"unexpected release checksum path {name!r}")
            checksums[name] = sha
        members = [entry.filename for entry in bundle.infolist() if not entry.is_dir()]
        if sorted(members) != sorted(["SHA256SUMS", *checksums]):
            raise ValueError("release does not contain exactly its checksum entries")
        for name, sha in checksums.items():
            content = bundle.read(name)
            if digest(content) != sha:
                raise ValueError(f"public release checksum mismatch for {name}")
            target = directory / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag", choices=RELEASES)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    args.evidence.mkdir(parents=True, exist_ok=True)
    commit, size, sha = RELEASES[args.tag]
    checked_commit = subprocess.check_output(
        ["git", "rev-parse", f"refs/tags/{args.tag}^{{commit}}"], cwd=ROOT, text=True,
    ).strip()
    if checked_commit != commit:
        raise ValueError("public release tag differs from the pinned revision")
    suffix = args.tag.removeprefix("sdk-")
    url = f"https://github.com/dev-null-GmbH/d0-sdk/releases/download/{args.tag}/d0-sdk-{suffix}.zip"
    raw = subprocess.check_output([
        "curl", "-fsSL", "--max-time", "60", "--max-filesize", str(size), url,
    ])
    with tempfile.TemporaryDirectory(prefix="d0-sdk-release-") as scratch:
        directory = Path(scratch)
        verify_archive(raw, size, sha, directory / "archives")
        source = directory / "source"
        source.mkdir()
        repository = subprocess.check_output(["git", "archive", commit], cwd=ROOT)
        with tarfile.open(fileobj=BytesIO(repository)) as archive:
            archive.extractall(source, filter="data")
        released = versions(source)
        scope = {
            "role": "supported distribution", "platform": "portable SDK packages",
            "release": args.tag, "revision": commit, "url": url, "size": size, "sha256": sha,
            "versions": released, "checkedAt": datetime.now(timezone.utc).isoformat(),
        }
        (args.evidence / "scope.json").write_text(json.dumps(scope, indent=2) + "\n")
        qualify(source, directory / "archives", released, None, evidence=args.evidence)


if __name__ == "__main__":
    main()
