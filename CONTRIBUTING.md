# Contributing to nobg

Thanks for taking the time to contribute. This project is small and the bar for
contributions is low — bug reports, suggestions, and pull requests are all welcome.

## Reporting bugs and requesting features

- Search [existing issues](https://github.com/soohanpark/nobg/issues) first to
  avoid duplicates.
- Use the **Bug report** or **Feature request** template when opening a new issue.
- For bugs, include: OS + version, Python version, `nobg --version`, the exact
  command you ran, and the full error output.

## Development setup

```bash
git clone https://github.com/soohanpark/nobg.git
cd nobg
uv sync --extra dev
uv run nobg --help
uv run pytest
```

If you don't have `uv`, install it from <https://docs.astral.sh/uv/> first.

## Pull request workflow

1. Fork the repository and create a feature branch from `main`.
2. Make focused changes — one logical change per PR.
3. Add or update tests for behavior changes. Keep `uv run pytest` green.
4. Update `CHANGELOG.md` under the `## [Unreleased]` section.
5. Open a PR using the template. Fill in the summary and check the boxes that apply.

### Commit messages

Conventional Commits style is preferred but not strictly enforced:

```
type: short description

Optional body explaining the why.
```

Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, `ci`, `perf`.

### Code style

- Python ≥ 3.11 compatible (the project supports 3.11 – 3.13).
- Keep functions small and focused. Match the surrounding style.
- Don't introduce abstractions for hypothetical future requirements.

## Releasing (maintainers)

The package version is derived from the git tag via `setuptools-scm`, so the
release flow is just:

1. Move the `## [Unreleased]` section in `CHANGELOG.md` under a new
   `## [X.Y.Z] - YYYY-MM-DD` heading; commit.
2. `git tag vX.Y.Z && git push origin main vX.Y.Z`.
3. The `Release` workflow runs the test matrix, builds the sdist + wheel
   (versioned `X.Y.Z` via `setuptools-scm`), and attaches both to a new
   GitHub Release.

PyPI publishing is intentionally not wired up. If we ever want it, add a
`pypi` job to `.github/workflows/release.yml` and register a Trusted
Publisher on PyPI for this repo.

## Code of conduct

Be kind. Assume good intent. This project follows the spirit of the
[Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
