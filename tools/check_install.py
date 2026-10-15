#!/usr/bin/env python3
"""Run customer examples from packed artifacts outside every source workspace."""

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

from verify_export import main as verify_export, versions

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ("auth", "platform", "accounting", "einvoice", "eric")


def run(*args, cwd, env=None):
    subprocess.run(args, cwd=cwd, env=env, check=True)


def go_proxy():
    proxy = ROOT / "dist/go"
    manifest = json.loads((ROOT / "export-manifest.json").read_text())
    release_versions = versions()
    for product in PRODUCTS:
        version = "v" + release_versions[product]
        module = f"github.com/dev-null-GmbH/d0-sdk/{product}/go"
        escaped = "".join("!" + char.lower() if char.isupper() else char for char in module)
        target = proxy / escaped / "@v"
        target.mkdir(parents=True, exist_ok=True)
        source = ROOT / product / "go"
        (target / f"{version}.mod").write_bytes((source / "go.mod").read_bytes())
        (target / f"{version}.info").write_text(json.dumps({"Version": version, "Time": "2026-10-15T00:00:00Z"}) + "\n")
        (target / "list").write_text(version + "\n")
        with zipfile.ZipFile(target / f"{version}.zip", "w", zipfile.ZIP_DEFLATED) as archive:
            for name in sorted(manifest["files"]):
                if not name.startswith(f"{product}/go/"):
                    continue
                path = ROOT / name
                entry = zipfile.ZipInfo(f"{module}@{version}/{path.relative_to(source).as_posix()}", (2026, 10, 15, 0, 0, 0))
                entry.external_attr = 0o100644 << 16
                archive.writestr(entry, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED)
    return proxy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public", action="store_true", help="install anonymous published versions instead of local artifacts")
    args = parser.parse_args()
    verify_export()
    release_versions = versions()
    proxy = None if args.public else go_proxy()
    with tempfile.TemporaryDirectory(prefix="d0-sdk-customer-") as directory:
        customer = Path(directory)
        node = customer / "node"
        node.mkdir()
        (node / "package.json").write_text('{"private":true,"type":"module"}\n')
        npm_packages = [f"@dev-null-gmbh/{'auth-machine' if product == 'auth' else product}@{release_versions[product]}" for product in PRODUCTS] if args.public else list(map(str, sorted((ROOT / "dist/npm").glob("*.tgz"))))
        run("npm", "install", "--ignore-scripts", "--no-audit", "--no-fund", "--registry", "https://registry.npmjs.org", *npm_packages, cwd=node)
        python = customer / "python"
        run("uv", "venv", "--python", "3.14.8", str(python), cwd=customer)
        interpreter = python / "bin/python"
        python_packages = [f"d0-{'auth-machine' if product == 'auth' else product}=={release_versions[product]}" for product in PRODUCTS] if args.public else list(map(str, sorted((ROOT / "dist/python").glob("*.whl"))))
        run("uv", "pip", "install", "--python", str(interpreter), "--default-index", "https://pypi.org/simple", *python_packages, cwd=customer)
        go = customer / "go"
        go.mkdir()
        env = {**os.environ, "GOWORK": "off", "GOMODCACHE": str(customer / "gomodcache"),
               "GOPROXY": f"{proxy.as_uri()},https://proxy.golang.org" if proxy else "https://proxy.golang.org",
               "GONOSUMDB": "github.com/dev-null-GmbH/d0-sdk" if proxy else "", "GOPRIVATE": "", "GONOPROXY": ""}
        run("go", "mod", "init", "sdk-install-check.invalid/customer", cwd=go, env=env)
        for product in PRODUCTS[1:]:
            js = (ROOT / product / "typescript/examples/fixture.mjs").read_text()
            assert '"../dist/index.js"' in js, product
            example = node / f"{product}.mjs"
            example.write_text(js.replace('"../dist/index.js"', f'"@dev-null-gmbh/{product}"'))
            run("node", str(example), cwd=node)
            py = customer / f"{product}.py"
            shutil.copyfile(ROOT / product / "python/examples/fixture.py", py)
            run(str(interpreter), "-I", str(py), cwd=customer)
            destination = go / product
            destination.mkdir()
            shutil.copyfile(ROOT / product / "go/examples/fixture/main.go", destination / "main.go")
            run("go", "mod", "edit", f"-require=github.com/dev-null-GmbH/d0-sdk/{product}/go@v{release_versions[product]}", cwd=go, env=env)
        run("go", "mod", "tidy", cwd=go, env=env)
        for product in PRODUCTS[1:]:
            run("go", "run", f"./{product}", cwd=go, env=env)
    print(f"all 12 product examples passed from {'public registries' if args.public else 'packed artifacts'} outside the workspace")


if __name__ == "__main__":
    main()
