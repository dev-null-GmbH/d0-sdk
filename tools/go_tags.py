#!/usr/bin/env python3
"""Retain immutable Go tags only when their complete module trees still match."""

import argparse
import os
import subprocess
from pathlib import Path

from verify_export import versions

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "dev-null-GmbH/d0-sdk"
REMOTE = f"https://github.com/{REPOSITORY}.git"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def matching_tree(commit, product):
    path = f"{product}/go"
    return git("rev-parse", f"{commit}:{path}") == git("rev-parse", f"HEAD:{path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    head = git("rev-parse", "HEAD")
    if args.publish and (os.environ.get("GITHUB_REPOSITORY") != REPOSITORY or
                         os.environ.get("GITHUB_REF") != "refs/heads/main" or
                         os.environ.get("RELEASE_SHA") != head):
        raise SystemExit("tag publication requires the qualified main commit")
    pending = []
    for product, version in versions(ROOT).items():
        ref = f"refs/tags/{product}/go/v{version}"
        current = git("ls-remote", "--refs", REMOTE, ref)
        if current:
            commit, actual_ref = current.split()
            if actual_ref != ref:
                raise SystemExit("unexpected remote tag")
            git("fetch", "--quiet", "--no-tags", REMOTE, commit)
            if not matching_tree(commit, product):
                raise SystemExit(f"immutable module collision: {ref}")
            print(f"verified existing module tree: {ref}")
        else:
            pending.append(ref)
    if args.publish:
        for ref in pending:
            subprocess.run(["gh", "api", "--method", "POST", f"repos/{REPOSITORY}/git/refs",
                            "-f", f"ref={ref}", "-f", f"sha={head}"], cwd=ROOT, check=True,
                           stdout=subprocess.DEVNULL)
            print(f"published {ref}")


if __name__ == "__main__":
    main()
