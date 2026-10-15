#!/usr/bin/env python3
"""Inspect the actual installable archives, not only workspace manifests."""

import hashlib
import json
import tarfile
import zipfile
from email.parser import BytesParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ("auth", "platform", "accounting", "einvoice", "eric")


def main():
    archives = []
    for product in PRODUCTS:
        suffix = "auth-machine" if product == "auth" else product
        package_name = f"@dev-null-gmbh/{suffix}"
        archive = ROOT / f"dist/npm/dev-null-gmbh-{suffix}-0.1.0.tgz"
        with tarfile.open(archive) as package:
            files = package.getnames()
            assert "package/dist/index.js" in files and "package/dist/index.d.ts" in files, product
            assert all(path == "package" or path.startswith("package/dist/") or path in {"package/package.json", "package/README.md", "package/LICENSE"} for path in files), files
            assert all(not member.issym() and not member.islnk() for member in package), product
            metadata = json.load(package.extractfile("package/package.json"))
            assert metadata["name"] == package_name and metadata["version"] == "0.1.0"
            assert metadata["license"] == "MIT"
            assert package.extractfile("package/LICENSE").read() == (ROOT / "LICENSE").read_bytes()
            if product != "auth":
                assert metadata["dependencies"]["@dev-null-gmbh/auth-machine"] == "0.1.0"
        archives.append(archive)
        module = "d0_auth_machine" if product == "auth" else f"d0_{product}"
        wheel = ROOT / f"dist/python/{module}-0.1.0-py3-none-any.whl"
        with zipfile.ZipFile(wheel) as package:
            assert f"{module}/py.typed" in package.namelist(), product
            metadata = BytesParser().parsebytes(package.read(f"{module}-0.1.0.dist-info/METADATA"))
            assert metadata["License-Expression"] == "MIT", product
            assert package.read(f"{module}-0.1.0.dist-info/licenses/LICENSE") == (ROOT / "LICENSE").read_bytes()
            if product != "auth":
                assert metadata.get_all("Requires-Dist") == ["d0-auth-machine==0.1.0"], product
            assert all(" @ " not in value for value in metadata.get_all("Requires-Dist", [])), product
        archives.extend([wheel, ROOT / f"dist/python/{module}-0.1.0.tar.gz"])
    archives.extend(path for path in (ROOT / "dist/go").rglob("*") if path.is_file())
    checksums = {str(path.relative_to(ROOT / "dist")): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(archives)}
    (ROOT / "dist/SHA256SUMS").write_text("".join(f"{digest}  {path}\n" for path, digest in checksums.items()))
    print(f"verified {len(archives)} installable archives, exact auth dependencies, Python typing and SHA256SUMS")


if __name__ == "__main__":
    main()
