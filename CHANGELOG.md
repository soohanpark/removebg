# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- One-line installer script (`install.sh`) that bootstraps `uv` and installs
  `nobg` from this GitHub repository.
- English `README.md` with badges, requirements matrix, and troubleshooting table.
  Korean version preserved as `README.ko.md`.
- `LICENSE` (MIT), `CONTRIBUTING.md`, `CHANGELOG.md`, GitHub issue and pull-request
  templates.
- `nobg --version` flag (`click.version_option`, sourced from package metadata).
- Test job in the release workflow: `pytest` runs against Python 3.9 – 3.13 on
  every `v*` tag push. The build / PyPI publish / GitHub Release jobs now run
  only after tests pass.

### Changed
- **Version is now derived from the git tag** via `setuptools-scm`. The
  `version` field was removed from `pyproject.toml` (replaced with
  `dynamic = ["version"]`), and `nobg/__init__.py` resolves `__version__`
  through `importlib.metadata`. Tagging `v0.2.0` and pushing is enough; no
  manual file edits are required for the version. Builds from non-tagged
  commits get a PEP 440 dev version such as `0.2.1.dev3+g<sha>`.
- Release workflow drops the manual "tag matches pyproject version" check
  (no longer applicable) in favor of a post-build assertion that the wheel
  filename matches the tag.

### Changed
- Primary install method is now `curl ... install.sh | sh` or
  `uv tool install git+https://github.com/soohanpark/nobg.git`. PyPI-based commands
  are no longer documented as the primary path because the package is not yet
  published on PyPI.
- Package renamed from `removebg` to `nobg` (module path, CLI entry point,
  pyproject metadata, release workflow URLs).

### Removed
- `packaging/homebrew/` Homebrew tap scaffolding and the related steps in the
  release workflow.

## [0.1.0] - 2026-04-22

### Added
- Initial CLI: single-image and recursive directory processing.
- Model selection (`u2net`, `u2netp`, `isnet-general-use`, `isnet-anime`,
  `birefnet-general`, `birefnet-portrait`, `silueta`, `sam`, `u2net_human_seg`,
  `u2net_cloth_seg`).
- Alpha matting with configurable `fg-threshold`, `bg-threshold`, `erode-size`.
- `--bgcolor`, `--only-mask`, `--post-process-mask`, `--overwrite` flags.
- GPU optional dependency group (`onnxruntime-gpu`).

[Unreleased]: https://github.com/soohanpark/nobg/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/soohanpark/nobg/releases/tag/v0.1.0
