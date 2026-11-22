"""Tests for archive_dir support (Loguru issue #1473)."""

import gzip
import zipfile
from pathlib import Path

import pytest

from logcraft import logger


def test_rotated_files_move_to_archive(tmp_path: Path) -> None:
    """Ротированные логи уезжают в отдельную папку."""
    main = tmp_path / "logs" / "app.log"
    main.parent.mkdir(parents=True)
    archive = tmp_path / "logs" / "archive"

    handler_id = logger.add(
        str(main),
        format="{message}",
        colorize=False,
        rotation=1,  # rotate before every next message
        archive_dir=str(archive),
    )
    logger.info("one")
    logger.info("two")
    logger.remove(handler_id)

    archived = list(archive.iterdir())
    assert len(archived) >= 1, "At least one rotated file should be archived"

    # Активный файл остаётся на месте, ротированные уехали
    leftovers = [p for p in main.parent.iterdir() if p.is_file() and p.name != "app.log"]
    assert leftovers == [], "No rotated files should remain in the main directory"


def test_archive_with_gz_compression(tmp_path: Path) -> None:
    """Архивные файлы сжимаются в gzip."""
    main = tmp_path / "logs" / "app.log"
    main.parent.mkdir(parents=True)
    archive = tmp_path / "logs" / "archive"

    handler_id = logger.add(
        str(main),
        format="{message}",
        colorize=False,
        rotation=1,
        archive_dir=str(archive),
        archive_compression="gz",
    )
    logger.info("payload")
    logger.info("second")
    logger.remove(handler_id)

    gz_files = list(archive.glob("*.gz"))
    assert gz_files, "At least one .gz file should be created"

    with gzip.open(gz_files[0], "rt", encoding="utf-8") as fh:
        content = fh.read()
        assert "payload" in content, "Archived content should be readable"


def test_archive_with_zip_compression(tmp_path: Path) -> None:
    """Архивные файлы упаковываются в zip."""
    main = tmp_path / "logs" / "app.log"
    main.parent.mkdir(parents=True)
    archive = tmp_path / "logs" / "archive"

    handler_id = logger.add(
        str(main),
        format="{message}",
        colorize=False,
        rotation=1,
        archive_dir=str(archive),
        archive_compression="zip",
    )
    logger.info("payload")
    logger.info("second")
    logger.remove(handler_id)

    zip_files = list(archive.glob("*.zip"))
    assert zip_files, "At least one .zip file should be created"

    with zipfile.ZipFile(zip_files[0], "r") as zf:
        names = zf.namelist()
        assert len(names) >= 1, "Zip should contain at least one file"
        with zf.open(names[0]) as f:
            content = f.read().decode("utf-8")
            assert "payload" in content, "Archived content should be readable"


def test_archive_rejects_explicit_compression(tmp_path: Path) -> None:
    """archive_dir нельзя комбинировать с явным compression=."""
    with pytest.raises(ValueError, match="cannot be combined"):
        logger.add(
            str(tmp_path / "x.log"),
            archive_dir=str(tmp_path / "arc"),
            compression="zip",
        )


def test_archive_rejects_non_file_sink() -> None:
    """archive_dir работает только с файловыми sink."""
    from io import StringIO

    with pytest.raises(ValueError, match="requires a file-path sink"):
        logger.add(StringIO(), archive_dir="arc")


def test_archive_unsupported_compression(tmp_path: Path) -> None:
    """Неподдерживаемые форматы сжатия вызывают ошибку."""
    with pytest.raises(ValueError, match="Unsupported archive compression"):
        logger.add(
            str(tmp_path / "x.log"),
            archive_dir=str(tmp_path / "arc"),
            archive_compression="rar",
        )


def test_archive_creates_directory_if_missing(tmp_path: Path) -> None:
    """Архивная папка создаётся автоматически."""
    main = tmp_path / "logs" / "app.log"
    main.parent.mkdir(parents=True)
    archive = tmp_path / "logs" / "archive" / "nested"  # не существует

    handler_id = logger.add(
        str(main),
        format="{message}",
        colorize=False,
        rotation=1,
        archive_dir=str(archive),
    )
    logger.info("one")
    logger.info("two")
    logger.remove(handler_id)

    assert archive.exists(), "Archive directory should be created automatically"
    assert list(archive.iterdir()), "Archive should contain at least one file"
