#!/usr/bin/env python3
"""Publish qualified archives with OIDC, refusing different bytes at an existing version."""

import base64
import hashlib
import json
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def integrity(data):
    return "sha512-" + base64.b64encode(hashlib.sha512(data).digest()).decode()


def main():
    if os.environ.get("GITHUB_REPOSITORY") != "dev-null-GmbH/d0-sdk" or os.environ.get("GITHUB_REF") != "refs/heads/main" or not os.environ.get("ACTIONS_ID_TOKEN_REQUEST_URL"):
        raise SystemExit("publication requires the configured main-branch OIDC workflow")
    pending = []
    for product in ("auth-machine", "platform", "accounting", "einvoice", "eric"):
        name = f"@dev-null-gmbh/{product}"
        archive = ROOT / f"dist/npm/dev-null-gmbh-{product}-0.1.0.tgz"
        url = f"https://registry.npmjs.org/{urllib.parse.quote(name, safe='')}/0.1.0"
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                body = response.read(1_048_577)
                if len(body) > 1_048_576:
                    raise SystemExit("registry metadata exceeds bound")
                metadata = json.loads(body)
        except urllib.error.HTTPError as error:
            if error.code != 404:
                raise SystemExit(f"registry preflight failed: HTTP {error.code}") from None
            pending.append(archive)
            continue
        if metadata.get("dist", {}).get("integrity") != integrity(archive.read_bytes()):
            raise SystemExit(f"immutable package collision: {name}@0.1.0")
        print(f"already published identical {name}@0.1.0")
    for archive in pending:
        subprocess.run(["npm", "publish", str(archive), "--access", "public", "--provenance", "--ignore-scripts", "--registry", "https://registry.npmjs.org"], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
