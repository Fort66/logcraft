"""Archive rotated log files into a separate directory (Loguru issue #1473)."""

from __future__ import annotations

import bz2
import gzip
import lzma
import shutil
import zipfile
from collections.abc import Callable
from pathlib import Path

SUPPORTED = ("gz", "bz2", "xz", "zip")


def make_archive_compression(
    sink_path: str | Path,
    archive_dir: str | Path,
    compression: str | None = None,
) -> Callable[[str], None]:
    """Build a loguru-compatible compression hook that archives rotated files.

    The active log file (same name as the sink) is left in place at sink stop;
    only rotated files (renamed by loguru with a date suffix) are moved.
    """
    if compression is not None and compression not in SUPPORTED:
        raise ValueError(
            f"Unsupported archive compression {compression!r}, expected one of {SUPPORTED}"
        )

    base_name = Path(sink_path).name
    archive = Path(archive_dir)

    def compressor(path: str) -> None:
        rotated = Path(path)
        if rotated.name == base_name:
            return  # active file at sink stop — keep it where it is

        archive.mkdir(parents=True, exist_ok=True)
        dest = archive / rotated.name
        if dest.exists():
            dest = archive / f"{rotated.stem}_{rotated.stat().st_mtime_ns}{rotated.suffix}"

        if compression is None:
            shutil.move(str(rotated), str(dest))
        elif compression == "zip":
            with zipfile.ZipFile(dest.with_suffix(".zip"), "w", zipfile.ZIP_DEFLATED) as zf:
                zf.write(rotated, arcname=rotated.name)
            rotated.unlink()
        else:
            target = dest.with_suffix(dest.suffix + "." + compression)
            with rotated.open("rb") as src:
                if compression == "gz":
                    with gzip.open(target, "wb") as dst:
                        shutil.copyfileobj(src, dst)
                elif compression == "bz2":
                    with bz2.open(target, "wb") as dst:
                        shutil.copyfileobj(src, dst)
                else:  # "xz"
                    with lzma.open(target, "wb") as dst:
                        shutil.copyfileobj(src, dst)
            rotated.unlink()

    return compressor
