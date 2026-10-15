#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

python3 tools/verify_export.py
python3 -m unittest discover -s tools
test "$(go env GOVERSION)" = go1.27.2
test "$(node --version)" = v26.10.0
test "$(npm --version)" = 12.2.0
test "$(uv --version | cut -d ' ' -f 2)" = 0.13.1

npm ci --ignore-scripts
uv sync --locked --all-packages --all-groups
npm run build --workspace @dev-null-gmbh/auth-machine
mkdir -p dist/npm dist/python

for product in auth platform accounting einvoice eric; do
  (cd "$product/go" && go test -race ./... && go vet ./...)
  if [ "$product" != auth ]; then
    (cd "$product/go" && go run ./examples/fixture)
  fi
  npm run check --workspace "./$product/typescript"
  npm test --workspace "./$product/typescript"
  npm run build --workspace "./$product/typescript"
  npm run example:fixture --if-present --workspace "./$product/typescript"
  npm pack --ignore-scripts --workspace "./$product/typescript" --pack-destination dist/npm >/dev/null
  (
    cd "$product/python"
    uv run --no-sync mypy src
    python_paths=(src tests)
    if [ -d examples ]; then python_paths+=(examples); fi
    uv run --no-sync ruff check "${python_paths[@]}"
    uv run --no-sync python -m unittest discover -s tests
    if [ "$product" != auth ]; then uv run --no-sync python examples/fixture.py; fi
  )
done
uv build --all-packages --no-sources --out-dir dist/python
python3 tools/verify_packages.py
python3 tools/check_install.py
python3 tools/verify_packages.py
