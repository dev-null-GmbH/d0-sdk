#!/usr/bin/env python3
"""Import only pinned, committed SDK files; no private checkout is needed by CI."""

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = {"go", "typescript", "python"}
SKIP = {"package-lock.json", "uv.lock", ".gitignore"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def exported(relative):
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("source path escape")
    if path.name in SKIP:
        return False
    return path.parts[0] in LANGUAGES | {"spec", "contracts"} or relative in {
        "CONTRACT.md", "operations.json"
    }


def transform(product, relative, data):
    if relative == "typescript/package.json":
        package = json.loads(data)
        package.pop("private", None)
        package["license"] = "MIT"
        package["files"] = ["dist", "README.md", "LICENSE"]
        if product != "auth":
            package["dependencies"]["@dev-null-gmbh/auth-machine"] = "0.1.0"
        package["publishConfig"] = {"registry": "https://registry.npmjs.org", "access": "public"}
        package["repository"] = {
            "type": "git", "url": "https://github.com/dev-null-GmbH/d0-sdk.git",
            "directory": f"{product}/typescript",
        }
        return (json.dumps(package, indent=2) + "\n").encode()
    if relative == "go/go.mod":
        lines = data.decode().splitlines()
        lines = [line for line in lines if not line.startswith((
            "replace github.com/dev-null-GmbH/d0-sdk/auth/go =>",
            "// Local qualification", "// Replace with an immutable",
        ))]
        result = "\n".join(lines).rstrip() + "\n"
        if "replace " in result or "../../../" in result:
            raise ValueError("unreviewed Go dependency override")
        return result.encode()
    if relative == "python/pyproject.toml":
        result = re.sub(
            r'd0-auth-machine = \{ path = "[^"]+" \}',
            'd0-auth-machine = { workspace = true }', data.decode(),
        )
        if "../../../" in result:
            raise ValueError("unreviewed Python dependency override")
        result = result.replace('[project]\n', '[project]\nlicense = "MIT"\nlicense-files = ["LICENSE"]\n', 1)
        return result.encode()
    return data


def collect(sources_root):
    sources = json.loads((ROOT / "sources.json").read_text())
    if set(sources) != {"auth", "platform", "accounting", "einvoice", "eric"}:
        raise ValueError("all five SDK sources must be pinned")
    output, records = {}, {}
    for product, source in sorted(sources.items()):
        repo = sources_root / source["repository"]
        commit, prefix = source["commit"], source["prefix"]
        if not re.fullmatch(r"[0-9a-f]{40}", commit):
            raise ValueError("source commit must be immutable")
        expected_prefix = "packages/machine" if product == "auth" else "sdk"
        if prefix != expected_prefix:
            raise ValueError("only the SDK source subtree may be exported")
        listing = git(repo, "ls-tree", "-rz", commit, "--", prefix).split(b"\0")
        for row in filter(None, listing):
            metadata, name = row.decode().split("\t", 1)
            mode, kind, blob = metadata.split()
            relative = name.removeprefix(prefix + "/")
            if not exported(relative):
                continue
            if kind != "blob" or mode not in {"100644", "100755"}:
                raise ValueError("links and special files are forbidden")
            data = git(repo, "cat-file", "blob", blob)
            transformed = transform(product, relative, data)
            destination = f"{product}/{relative}"
            output[destination] = transformed
            records[destination] = {
                "sourcePath": name, "sourceSha256": sha(data),
                "sha256": sha(transformed), "transformed": data != transformed,
            }
        for language in sorted(LANGUAGES):
            if not any(path.startswith(f"{product}/{language}/") for path in output):
                raise ValueError(f"missing {product}/{language} source")
            name = f"{product}/{language}/LICENSE"
            license_text = (ROOT / "LICENSE").read_bytes()
            output[name] = license_text
            records[name] = {"origin": "distribution-license", "sourcePath": "LICENSE",
                             "sourceSha256": sha(license_text), "sha256": sha(license_text),
                             "transformed": False}
    manifest = {"schemaVersion": 1, "sources": sources, "files": records}
    output["export-manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources-root", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = collect(args.sources_root.resolve())
    old = ROOT / "export-manifest.json"
    previous = json.loads(old.read_text())["files"] if old.exists() else {}
    stale = set(previous) - set(output)
    if args.check:
        changed = [name for name, data in output.items() if not (ROOT / name).is_file() or (ROOT / name).read_bytes() != data]
        if changed or stale:
            raise SystemExit(f"SDK export drift: {sorted(set(changed) | stale)}")
    else:
        for name in stale:
            (ROOT / name).unlink()
        for name, data in output.items():
            target = ROOT / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    print(f"verified {len(output) - 1} public SDK files from five pinned sources")


if __name__ == "__main__":
    main()
