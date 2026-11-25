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


def run(*args, cwd, env=None, stdout=None):
    subprocess.run(args, cwd=cwd, env=env, stdout=stdout, check=True)


def escape_module(module):
    return "".join("!" + char.lower() if char.isupper() else char for char in module)


def zip_files(path):
    with zipfile.ZipFile(path) as module:
        names = [name for name in module.namelist() if not name.endswith("/")]
        assert len(names) == len(set(names)), path
        return {name: module.read(name) for name in names}


def go_proxy():
    proxy = ROOT / "dist/go"
    manifest = json.loads((ROOT / "export-manifest.json").read_text())
    release_versions = versions()
    for product in PRODUCTS:
        version = "v" + release_versions[product]
        module = f"github.com/dev-null-GmbH/d0-sdk/{product}/go"
        target = proxy / escape_module(module) / "@v"
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


def qualify(source, archives, release_versions, proxy, public_registries=False, evidence=None):
    if evidence:
        evidence.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="d0-sdk-customer-") as directory:
        customer = Path(directory)
        node = customer / "node"
        node.mkdir()
        (node / "package.json").write_text('{"private":true,"type":"module"}\n')
        npm_packages = [f"@dev-null-gmbh/{'auth-machine' if product == 'auth' else product}@{release_versions[product]}" for product in PRODUCTS] if public_registries else list(map(str, sorted((archives / "npm").glob("*.tgz"))))
        run("npm", "install", "--ignore-scripts", "--no-audit", "--no-fund", "--registry", "https://registry.npmjs.org", *npm_packages, cwd=node)
        python = customer / "python"
        run("uv", "venv", "--python", "3.14.10", str(python), cwd=customer)
        interpreter = python / "bin/python"
        python_packages = [f"d0-{'auth-machine' if product == 'auth' else product}=={release_versions[product]}" for product in PRODUCTS] if public_registries else list(map(str, sorted((archives / "python").glob("*.whl"))))
        run("uv", "pip", "install", "--python", str(interpreter), "--default-index", "https://pypi.org/simple", *python_packages, cwd=customer)
        go = customer / "go"
        go.mkdir()
        env = {**os.environ, "GOWORK": "off", "GOMODCACHE": str(customer / "gomodcache"),
               "GOPROXY": f"{proxy.as_uri()},https://proxy.golang.org" if proxy else "https://proxy.golang.org",
               "GONOSUMDB": "github.com/dev-null-GmbH/d0-sdk" if proxy else "", "GOSUMDB": "sum.golang.org", "GOPRIVATE": "", "GONOPROXY": ""}
        run("go", "mod", "init", "sdk-install-check.invalid/customer", cwd=go, env=env)
        for product in PRODUCTS[1:]:
            js = (source / product / "typescript/examples/fixture.mjs").read_text()
            assert '"../dist/index.js"' in js, product
            example = node / f"{product}.mjs"
            example.write_text(js.replace('"../dist/index.js"', f'"@dev-null-gmbh/{product}"'))
            run("node", str(example), cwd=node)
            py = customer / f"{product}.py"
            shutil.copyfile(source / product / "python/examples/fixture.py", py)
            run(str(interpreter), "-I", str(py), cwd=customer)
            destination = go / product
            destination.mkdir()
            shutil.copyfile(source / product / "go/examples/fixture/main.go", destination / "main.go")
            run("go", "mod", "edit", f"-require=github.com/dev-null-GmbH/d0-sdk/{product}/go@v{release_versions[product]}", cwd=go, env=env)
        run("go", "mod", "tidy", cwd=go, env=env)
        if evidence:
            shutil.copyfile(node / "package-lock.json", evidence / "package-lock.json")
            shutil.copyfile(go / "go.mod", evidence / "go.mod")
            shutil.copyfile(go / "go.sum", evidence / "go.sum")
            with (evidence / "requirements.txt").open("w") as report:
                run("uv", "pip", "list", "--format", "freeze", "--python", str(interpreter), cwd=customer, stdout=report)
            with (evidence / "modules.json").open("w") as report:
                run("go", "list", "-m", "-json", "all", cwd=go, env=env, stdout=report)
            with (evidence / "modules-download.json").open("w") as report:
                run("go", "mod", "download", "-json", "all", cwd=go, env=env, stdout=report)
            for product, version in release_versions.items():
                module = f"github.com/dev-null-GmbH/d0-sdk/{product}/go"
                download = json.loads(subprocess.check_output(
                    ("go", "mod", "download", "-json", f"{module}@v{version}"), cwd=go, env=env,
                ))
                if proxy is None and not public_registries:
                    archived = archives / "go" / escape_module(module) / "@v"
                    assert (archived / f"v{version}.mod").read_bytes() == Path(download["GoMod"]).read_bytes(), module
                    assert zip_files(archived / f"v{version}.zip") == zip_files(download["Zip"]), module
                metadata = evidence / "declared-go" / product
                metadata.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(download["GoMod"], metadata / "go.mod")
        for product in PRODUCTS[1:]:
            run("go", "run", f"./{product}", cwd=go, env=env)
    print(f"all 12 product examples passed from {'public registries' if public_registries else 'packed artifacts'} outside the workspace")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public", action="store_true", help="install anonymous published versions instead of local artifacts")
    parser.add_argument("--evidence-dir", type=Path, help="record the clean consumer dependency graphs")
    args = parser.parse_args()
    verify_export()
    proxy = None if args.public else go_proxy()
    qualify(ROOT, ROOT / "dist", versions(), proxy, args.public, args.evidence_dir)


if __name__ == "__main__":
    main()
