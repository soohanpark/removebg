from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from PIL import Image
from rembg import new_session, remove

SUPPORTED_INPUT_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}


@dataclass
class RemoveOptions:
    model: str = "u2net"
    alpha_matting: bool = False
    alpha_matting_foreground_threshold: int = 240
    alpha_matting_background_threshold: int = 10
    alpha_matting_erode_size: int = 10
    post_process_mask: bool = False
    only_mask: bool = False
    bgcolor: tuple[int, int, int, int] | None = None


def remove_background(input_bytes: bytes, options: RemoveOptions, session=None) -> bytes:
    session = session or new_session(options.model)
    return remove(
        input_bytes,
        session=session,
        alpha_matting=options.alpha_matting,
        alpha_matting_foreground_threshold=options.alpha_matting_foreground_threshold,
        alpha_matting_background_threshold=options.alpha_matting_background_threshold,
        alpha_matting_erode_size=options.alpha_matting_erode_size,
        post_process_mask=options.post_process_mask,
        only_mask=options.only_mask,
        bgcolor=options.bgcolor,
    )


def process_file(src: Path, dst: Path, options: RemoveOptions, session=None) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)

    with src.open("rb") as f:
        data = f.read()

    output = remove_background(data, options, session=session)

    suffix = dst.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        img = Image.open(BytesIO(output)).convert("RGBA")
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        background.save(dst, format="JPEG", quality=95)
    else:
        with dst.open("wb") as f:
            f.write(output)
    return dst


def iter_images(path: Path, recursive: bool = False):
    if path.is_file():
        if path.suffix.lower() in SUPPORTED_INPUT_EXTS:
            yield path
        return
    pattern = "**/*" if recursive else "*"
    for p in sorted(path.glob(pattern)):
        if p.is_file() and p.suffix.lower() in SUPPORTED_INPUT_EXTS:
            yield p


def resolve_output_path(src: Path, input_root: Path, output: Path | None) -> Path:
    if output is None:
        return src.with_name(f"{src.stem}_nobg.png")

    if input_root.is_file():
        if output.suffix:
            return output
        output.mkdir(parents=True, exist_ok=True)
        return output / f"{src.stem}_nobg.png"

    rel = src.relative_to(input_root)
    return (output / rel).with_suffix(".png")
