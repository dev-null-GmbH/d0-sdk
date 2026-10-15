#!/usr/bin/env python3
"""Publish Python archives with OIDC after checking all existing version bytes."""

import hashlib
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

from verify_export import versions

ROOT = Path(__file__).resolve().parents[1]


def main():
    if os.environ.get("GITHUB_REPOSITORY") != "dev-null-GmbH/d0-sdk" or os.environ.get("GITHUB_REF") != "refs/heads/main" or not os.environ.get("ACTIONS_ID_TOKEN_REQUEST_URL"):
        raise SystemExit("publication requires the configured main-branch OIDC workflow")
    pending = []
    for product, version in versions(ROOT).items():
        name = "d0-auth-machine" if product == "auth" else f"d0-{product}"
        module = name.replace("-", "_")
        archives = [ROOT / f"dist/python/{module}-{version}{suffix}"
                    for suffix in ("-py3-none-any.whl", ".tar.gz")]
        try:
            with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/{version}/json", timeout=30) as response:
                body = response.read(1_048_577)
                if len(body) > 1_048_576:
                    raise SystemExit("registry metadata exceeds bound")
                existing = {item["filename"]: item for item in json.loads(body)["urls"]}
        except urllib.error.HTTPError as error:
            if error.code != 404:
                raise SystemExit(f"registry preflight failed: HTTP {error.code}") from None
            existing = {}
        if set(existing) - {archive.name for archive in archives}:
            raise SystemExit(f"unreviewed files at immutable package version: {name}=={version}")
        for archive in archives:
            digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            if archive.name not in existing:
                pending.append(archive)
            elif existing[archive.name].get("yanked") or existing[archive.name].get("digests", {}).get("sha256") != digest:
                raise SystemExit(f"immutable package collision: {archive.name}")
            else:
                print(f"already published identical {archive.name}")
    for archive in pending:
        subprocess.run(["uv", "publish", "--trusted-publishing", "always", str(archive)], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
