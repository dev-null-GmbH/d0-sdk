#!/usr/bin/env python3
"""Verify SDK provenance and public dependency metadata without private sources."""

import hashlib
import json
import re
import subprocess
import tomllib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ("auth", "platform", "accounting", "einvoice", "eric")
DISTRIBUTION_FILES = {
    ".github/workflows/release.yml", ".gitignore", ".python-version", "AGENTS.md",
    "LICENSE", "README.md", "PUBLISHING.md", "export-manifest.json", "sources.json",
    "go.work", "package.json", "package-lock.json", "pyproject.toml", "uv.lock",
    "tools/check.sh", "tools/check_install.py", "tools/import_sources.py",
    "tools/publish_npm.py", "tools/verify_export.py", "tools/verify_packages.py",
    "tools/test_import_sources.py", "tools/test_publish_npm.py",
}


def verify_inventory(actual, expected):
    assert actual == expected, f"public file inventory drift: extra={sorted(actual - expected)}, missing={sorted(expected - actual)}"


def main():
    manifest = json.loads((ROOT / "export-manifest.json").read_text())
    assert manifest["schemaVersion"] == 1
    assert manifest["sources"] == json.loads((ROOT / "sources.json").read_text())
    assert set(manifest["sources"]) == set(PRODUCTS)
    files = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT)
    actual = {name.decode() for name in files.split(b"\0") if name}
    verify_inventory(actual, set(manifest["files"]) | DISTRIBUTION_FILES)
    for name, record in manifest["files"].items():
        path = PurePosixPath(name)
        assert not path.is_absolute() and ".." not in path.parts and path.parts[0] in PRODUCTS
        target = ROOT / name
        assert target.is_file() and not target.is_symlink(), name
        assert hashlib.sha256(target.read_bytes()).hexdigest() == record["sha256"], name
        assert re.fullmatch(r"[0-9a-f]{64}", record["sourceSha256"]), name
    for product in PRODUCTS:
        package = json.loads((ROOT / product / "typescript/package.json").read_text())
        assert package["version"] == "0.1.0" and not package.get("private"), product
        assert package["license"] == "MIT"
        assert package["publishConfig"] == {"registry": "https://registry.npmjs.org", "access": "public"}
        assert all(re.fullmatch(r"\d+\.\d+\.\d+", value) for value in package["dependencies"].values()), product
        metadata = tomllib.loads((ROOT / product / "python/pyproject.toml").read_text())
        assert metadata["project"]["version"] == "0.1.0"
        assert metadata["project"]["license"] == "MIT"
        assert metadata["project"]["license-files"] == ["LICENSE"]
        for language in ("go", "typescript", "python"):
            assert (ROOT / product / language / "LICENSE").read_bytes() == (ROOT / "LICENSE").read_bytes()
        if product != "auth":
            assert package["dependencies"]["@dev-null-gmbh/auth-machine"] == "0.1.0"
            assert metadata["project"]["dependencies"] == ["d0-auth-machine==0.1.0"]
            assert metadata["tool"]["uv"]["sources"]["d0-auth-machine"] == {"workspace": True}
        module = (ROOT / product / "go/go.mod").read_text()
        assert module.startswith(f"module github.com/dev-null-GmbH/d0-sdk/{product}/go\n"), product
        assert "replace " not in module and "../../../" not in module, product
    print(f"verified {len(manifest['files'])} pinned files and all 15 public package identities")


if __name__ == "__main__":
    main()
