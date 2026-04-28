#!/usr/bin/env bash
# Regenerate the Homebrew `resource` blocks for the removebg formula.
#
# Spliced into Formula/removebg.rb between the BEGIN_RESOURCES /
# END_RESOURCES markers.
#
# Requirements:
#   - python3 (3.9+)
#   - internet access (PyPI)
#
# Usage:
#   ./packaging/homebrew/generate-resources.sh
#
# After running, also update `sha256` in Formula/removebg.rb with:
#   curl -sL https://github.com/soohanpark/removebg/archive/refs/tags/vX.Y.Z.tar.gz | shasum -a 256
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
HERE="$REPO_ROOT/packaging/homebrew"
FORMULA="$HERE/Formula/removebg.rb"
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

python3 -m venv "$WORKDIR/venv"
# shellcheck disable=SC1091
source "$WORKDIR/venv/bin/activate"

pip install --quiet --upgrade pip
# `packaging` provides Requirement/marker parsing for collect_resources.py.
pip install --quiet packaging
pip install --quiet "$REPO_ROOT"

python3 "$HERE/collect_resources.py" > "$WORKDIR/resources.rb"

echo "--- generated resources ---"
cat "$WORKDIR/resources.rb"
echo "--- end ---"

# Splice into the formula between markers.
python3 - "$FORMULA" "$WORKDIR/resources.rb" <<'PY'
import sys, pathlib
formula_path, resources_path = map(pathlib.Path, sys.argv[1:3])
formula = formula_path.read_text()
resources = resources_path.read_text().rstrip() + "\n"
begin = "  # BEGIN_RESOURCES\n"
end = "  # END_RESOURCES\n"
i = formula.index(begin) + len(begin)
j = formula.index(end)
formula_path.write_text(formula[:i] + resources + formula[j:])
print(f"updated {formula_path}")
PY

echo
echo "Next: update the sha256 in $FORMULA, then run:"
echo "  brew install --build-from-source $FORMULA"
echo "  brew test removebg"
echo "  brew audit --strict --new-formula removebg"
