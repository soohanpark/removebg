"""Print Homebrew `resource` blocks for removebg's runtime dependencies.

Walks the runtime dependency graph of `removebg` in the currently active
Python environment, then queries PyPI for each dependency's source
distribution (preferred) or first wheel and emits Homebrew-formatted
`resource ... do ... end` blocks to stdout.

Run from inside a venv that has `removebg` installed. Output is meant to
be spliced into the Formula between BEGIN_RESOURCES / END_RESOURCES
markers by `generate-resources.sh`.
"""
from __future__ import annotations

import json
import sys
from importlib.metadata import PackageNotFoundError, distribution, requires
from urllib.request import urlopen

from packaging.markers import default_environment
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = "removebg"


def walk(name: str, seen: set[str]) -> None:
    name = canonicalize_name(name)
    if name in seen:
        return
    seen.add(name)
    try:
        reqs = requires(name) or []
    except PackageNotFoundError:
        return
    env = default_environment()
    for req_str in reqs:
        req = Requirement(req_str)
        if req.marker and not req.marker.evaluate(env):
            continue
        walk(req.name, seen)


def fetch_release(name: str, version: str) -> tuple[str, str, str]:
    with urlopen(f"https://pypi.org/pypi/{name}/{version}/json") as r:
        data = json.load(r)
    files = data.get("urls", [])
    for f in files:
        if f.get("packagetype") == "sdist":
            return f["url"], f["digests"]["sha256"], "sdist"
    if files:
        f = files[0]
        return f["url"], f["digests"]["sha256"], "wheel"
    raise RuntimeError(f"no distribution files for {name}=={version}")


def main() -> int:
    seen: set[str] = set()
    walk(ROOT, seen)
    seen.discard(canonicalize_name(ROOT))

    blocks: list[str] = []
    wheel_only: list[str] = []
    for name in sorted(seen):
        try:
            dist = distribution(name)
        except PackageNotFoundError:
            print(f"# warning: {name} not installed; skipping", file=sys.stderr)
            continue
        canonical = dist.metadata["Name"]
        version = dist.version
        url, sha, kind = fetch_release(canonical, version)
        if kind == "wheel":
            wheel_only.append(canonical)
        blocks.append(
            f'  resource "{canonical}" do\n'
            f'    url "{url}"\n'
            f'    sha256 "{sha}"\n'
            f"  end"
        )
    print("\n\n".join(blocks))

    if wheel_only:
        print(
            "\n# WARNING: the following packages publish wheels only. The URL "
            "above points to one wheel for the current platform; for a portable "
            "Homebrew formula you must split into `on_macos` / `on_linux` / "
            "`on_arm` blocks with platform-specific wheel URLs:\n#   "
            + ", ".join(wheel_only),
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
