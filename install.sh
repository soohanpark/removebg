#!/bin/sh
# nobg installer — one-line install for macOS / Linux.
#
#   curl -LsSf https://raw.githubusercontent.com/soohanpark/nobg/main/install.sh | sh
#
# Installs uv if missing, then installs nobg from this GitHub repo as a uv tool.
# Re-running the script upgrades nobg to the latest commit on the default branch.

set -eu

REPO_URL="${NOBG_REPO_URL:-git+https://github.com/soohanpark/nobg.git}"
UV_INSTALLER="https://astral.sh/uv/install.sh"

say() { printf '\033[1;32m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m==>\033[0m %s\n' "$*" >&2; }
die() { printf '\033[1;31m==>\033[0m %s\n' "$*" >&2; exit 1; }

have() { command -v "$1" >/dev/null 2>&1; }

ensure_uv() {
  if have uv; then
    say "uv already installed ($(uv --version))"
    return
  fi
  say "uv not found — installing via $UV_INSTALLER"
  curl -LsSf "$UV_INSTALLER" | sh

  # uv's installer drops the binary into ~/.local/bin (or $XDG_BIN_HOME).
  # That dir may not be on PATH for this shell yet, so add it before we call uv.
  for candidate in "${XDG_BIN_HOME:-}" "$HOME/.local/bin" "$HOME/.cargo/bin"; do
    [ -n "$candidate" ] && [ -d "$candidate" ] && PATH="$candidate:$PATH"
  done
  export PATH

  have uv || die "uv install failed: 'uv' still not on PATH. Open a new shell and re-run, or install uv manually from https://docs.astral.sh/uv/"
}

install_nobg() {
  say "Installing nobg from $REPO_URL"
  # --force so re-running the installer upgrades cleanly.
  uv tool install --force "$REPO_URL"
}

post_install_hint() {
  if have nobg; then
    say "Installed: $(nobg --version 2>/dev/null || echo nobg)"
    say "Try it:    nobg --help"
    return
  fi
  warn "'nobg' is installed but not yet on this shell's PATH."
  warn "Run:  uv tool update-shell"
  warn "Then open a new terminal, or:  exec \$SHELL -l"
}

main() {
  have curl || die "curl is required. Install curl and re-run."
  ensure_uv
  install_nobg
  post_install_hint
}

main "$@"
