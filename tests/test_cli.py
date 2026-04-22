from pathlib import Path

from click.testing import CliRunner

from removebg.cli import main
from removebg.core import iter_images, resolve_output_path


def test_help_shows_usage():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Remove backgrounds from images" in result.output


def test_iter_images_filters_by_extension(tmp_path: Path):
    (tmp_path / "a.png").write_bytes(b"")
    (tmp_path / "b.JPG").write_bytes(b"")
    (tmp_path / "c.txt").write_bytes(b"")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "d.webp").write_bytes(b"")

    flat = list(iter_images(tmp_path, recursive=False))
    assert {p.name for p in flat} == {"a.png", "b.JPG"}

    deep = list(iter_images(tmp_path, recursive=True))
    assert {p.name for p in deep} == {"a.png", "b.JPG", "d.webp"}


def test_resolve_output_path_defaults_next_to_input(tmp_path: Path):
    src = tmp_path / "photo.jpg"
    src.write_bytes(b"")
    out = resolve_output_path(src, src, None)
    assert out == tmp_path / "photo_nobg.png"


def test_resolve_output_path_directory_mirrors_structure(tmp_path: Path):
    root = tmp_path / "in"
    root.mkdir()
    sub = root / "a"
    sub.mkdir()
    src = sub / "x.png"
    src.write_bytes(b"")

    out_root = tmp_path / "out"
    result = resolve_output_path(src, root, out_root)
    assert result == out_root / "a" / "x.png"
