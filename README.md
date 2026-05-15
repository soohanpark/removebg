# nobg

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%E2%80%933.13-blue.svg)](pyproject.toml)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](#requirements)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A tiny CLI that removes backgrounds from images. Built on top of
[`rembg`](https://github.com/danielgatis/rembg) (U²-Net / BiRefNet / ISNet / SAM).

> 한국어 문서는 [README.ko.md](README.ko.md)를 참고하세요.

## Quick install (one-liner)

macOS / Linux:

```bash
curl -LsSf https://raw.githubusercontent.com/soohanpark/nobg/main/install.sh | sh
```

The installer bootstraps [`uv`](https://docs.astral.sh/uv/) if missing and installs `nobg`
as an isolated tool from this repository. Re-run it any time to upgrade to the latest commit.

> **⚠️ If `uv` was installed for the first time by this script, open a new terminal before using `nobg`.**
> The `uv` installer appends `~/.local/bin` to your shell rc (`~/.zshrc` / `~/.bashrc`),
> but the change is not picked up by the *current* shell. Pick one:
>
> - Open a new terminal tab/window (easiest)
> - Run `exec $SHELL -l` in the current shell
> - Or `source ~/.zshrc` (bash users: `source ~/.bashrc`)
>
> If you already had `uv` installed, you can call `nobg` immediately in the same shell.

Once ready:

```bash
nobg --help
nobg photo.jpg                # produces photo_nobg.png
```

If `nobg: command not found` still appears, run `uv tool update-shell` and reopen the terminal.

## Other install methods

If `uv` is already installed:

```bash
uv tool install git+https://github.com/soohanpark/nobg.git
```

Zero-install, one-shot:

```bash
uvx --from git+https://github.com/soohanpark/nobg.git nobg input.jpg
```

`pipx`:

```bash
pipx install git+https://github.com/soohanpark/nobg.git
```

GPU (CUDA) build:

```bash
uv tool install --with onnxruntime-gpu git+https://github.com/soohanpark/nobg.git
```

> Requires the CUDA toolkit to already be installed on your system.

Upgrade / uninstall:

```bash
uv tool upgrade nobg
uv tool uninstall nobg
# pipx equivalents: pipx upgrade nobg / pipx uninstall nobg
```

### Requirements

- Internet access on first run (model weights are cached under `~/.u2net/`).
- ~2 GB of free disk space (models + dependencies).
- Python ≥ 3.9 (you don't need it installed — `uv` will fetch one).
- macOS, Linux, or Windows. On Windows, install `uv` via PowerShell with
  `irm https://astral.sh/uv/install.ps1 | iex`, then use the `uv tool install ...` command above.

## Usage

```bash
# Single image
nobg photo.jpg

# Custom output path
nobg photo.jpg -o out.png

# Batch a directory
nobg ./photos -o ./out

# Recurse into subdirectories
nobg ./photos -o ./out -r

# Pick a different model (anime / portrait / etc.)
nobg photo.jpg -m isnet-anime
nobg portrait.jpg -m birefnet-portrait

# Smoother edges (slower) via alpha matting
nobg photo.jpg --alpha-matting

# Fill the background with a solid color instead of transparency
nobg photo.jpg --bgcolor 255,255,255

# Output only the alpha mask
nobg photo.jpg --only-mask
```

## Options

| Flag | Description |
| --- | --- |
| `-o, --output` | Output file or directory. Defaults to `<name>_nobg.png` next to the input. |
| `-m, --model` | Segmentation model (`u2net`, `u2netp`, `isnet-general-use`, `isnet-anime`, `birefnet-general`, `birefnet-portrait`, `silueta`, `sam`, ...). |
| `-r, --recursive` | Recurse into subdirectories. |
| `--alpha-matting` | Enable alpha matting (smoother edges, slower). |
| `--fg-threshold`, `--bg-threshold`, `--erode-size` | Alpha-matting parameters. |
| `--post-process-mask` | Apply morphological post-processing to the mask. |
| `--only-mask` | Write the alpha mask instead of the cutout. |
| `--bgcolor R,G,B[,A]` | Fill the background with a solid color. |
| `--overwrite` | Overwrite existing output files. |

## Supported formats

- **Input**: `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tiff`, `.tif`
- **Output**: `.png` by default (transparency preserved). For `.jpg` / `.jpeg`, the cutout is composited onto a white background.

## Programmatic API

```python
from pathlib import Path
from nobg.core import RemoveOptions, process_file

process_file(
    src=Path("input.jpg"),
    dst=Path("output.png"),
    options=RemoveOptions(model="u2net"),
)
```

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `command not found: nobg` | Run `uv tool update-shell`, then open a new shell. |
| `error: externally-managed-environment` | Don't `pip install` into the system Python. Use one of the `uv` / `pipx` methods above. |
| First run is slow | The model is being downloaded — subsequent runs use the cache. |
| `No supported images found` | Use a supported extension: `.jpg .jpeg .png .webp .bmp .tiff .tif`. |
| Rough edges | Try `-m birefnet-general` or add `--alpha-matting`. |
| CUDA not used | Reinstall with `--with onnxruntime-gpu`. |

## Development

```bash
git clone https://github.com/soohanpark/nobg.git
cd nobg
uv sync --extra dev
uv run nobg --help
uv run pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Uninstall

```bash
uv tool uninstall nobg            # or: pipx uninstall nobg
rm -rf ~/.u2net                   # also clear the cached model weights
```

## Acknowledgements

`nobg` is a thin CLI wrapper around the excellent
[`rembg`](https://github.com/danielgatis/rembg) library by Daniel Gatis and contributors.
Segmentation models come from
[U²-Net](https://github.com/xuebinqin/U-2-Net),
[BiRefNet](https://github.com/ZhengPeng7/BiRefNet),
[IS-Net](https://github.com/xuebinqin/DIS),
and [Segment Anything](https://github.com/facebookresearch/segment-anything).

## License

Released under the [MIT License](LICENSE).
