from __future__ import annotations

import sys
from pathlib import Path

import click
from rembg import new_session

from .core import (
    RemoveOptions,
    iter_images,
    process_file,
    resolve_output_path,
)

AVAILABLE_MODELS = [
    "u2net",
    "u2netp",
    "u2net_human_seg",
    "u2net_cloth_seg",
    "silueta",
    "isnet-general-use",
    "isnet-anime",
    "sam",
    "birefnet-general",
    "birefnet-portrait",
]


def _parse_bgcolor(value: str | None) -> tuple[int, int, int, int] | None:
    if not value:
        return None
    parts = [p.strip() for p in value.split(",")]
    if len(parts) not in (3, 4):
        raise click.BadParameter("bgcolor must be 'R,G,B' or 'R,G,B,A'")
    try:
        nums = [int(p) for p in parts]
    except ValueError as exc:
        raise click.BadParameter("bgcolor values must be integers 0-255") from exc
    if any(n < 0 or n > 255 for n in nums):
        raise click.BadParameter("bgcolor values must be between 0 and 255")
    if len(nums) == 3:
        nums.append(255)
    return tuple(nums)  # type: ignore[return-value]


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument(
    "input_path",
    type=click.Path(exists=True, path_type=Path, readable=True),
)
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    default=None,
    help="Output file or directory. Defaults to '<name>_nobg.png' next to the input.",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(AVAILABLE_MODELS, case_sensitive=False),
    default="u2net",
    show_default=True,
    help="Segmentation model to use.",
)
@click.option(
    "-r",
    "--recursive",
    is_flag=True,
    help="Recurse into subdirectories when input is a directory.",
)
@click.option(
    "--alpha-matting/--no-alpha-matting",
    default=False,
    help="Enable alpha matting for smoother edges (slower).",
)
@click.option("--fg-threshold", type=int, default=240, show_default=True)
@click.option("--bg-threshold", type=int, default=10, show_default=True)
@click.option("--erode-size", type=int, default=10, show_default=True)
@click.option(
    "--post-process-mask",
    is_flag=True,
    help="Apply morphological post-processing to the predicted mask.",
)
@click.option(
    "--only-mask",
    is_flag=True,
    help="Output the alpha mask instead of the cutout image.",
)
@click.option(
    "--bgcolor",
    type=str,
    default=None,
    help="Solid background color 'R,G,B' or 'R,G,B,A' instead of transparency.",
)
@click.option(
    "--overwrite/--no-overwrite",
    default=False,
    help="Overwrite existing output files.",
)
def main(
    input_path: Path,
    output: Path | None,
    model: str,
    recursive: bool,
    alpha_matting: bool,
    fg_threshold: int,
    bg_threshold: int,
    erode_size: int,
    post_process_mask: bool,
    only_mask: bool,
    bgcolor: str | None,
    overwrite: bool,
) -> None:
    """Remove backgrounds from images.

    INPUT_PATH can be a single image or a directory of images.
    """
    options = RemoveOptions(
        model=model.lower(),
        alpha_matting=alpha_matting,
        alpha_matting_foreground_threshold=fg_threshold,
        alpha_matting_background_threshold=bg_threshold,
        alpha_matting_erode_size=erode_size,
        post_process_mask=post_process_mask,
        only_mask=only_mask,
        bgcolor=_parse_bgcolor(bgcolor),
    )

    images = list(iter_images(input_path, recursive=recursive))
    if not images:
        click.echo(f"No supported images found in {input_path}", err=True)
        sys.exit(1)

    click.echo(f"Loading model '{options.model}'...")
    session = new_session(options.model)

    failures = 0
    with click.progressbar(images, label="Removing backgrounds") as bar:
        for src in bar:
            dst = resolve_output_path(src, input_path, output)
            if dst.exists() and not overwrite:
                click.echo(f"\nSkip (exists): {dst}", err=True)
                continue
            try:
                process_file(src, dst, options, session=session)
            except Exception as exc:  # noqa: BLE001
                failures += 1
                click.echo(f"\nFailed: {src} -> {exc}", err=True)

    total = len(images)
    click.echo(f"Done. Processed {total - failures}/{total} image(s).")
    if failures:
        sys.exit(2)


if __name__ == "__main__":
    main()
