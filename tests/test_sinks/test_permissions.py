"""Tests for permissions= on file sinks (Loguru issue #401)."""

import os
import stat
from pathlib import Path

import pytest

from logcraft import logger


def mode_of(path: Path) -> int:
    return stat.S_IMODE(os.stat(path).st_mode)


def test_permissions_applied_at_add(tmp_path: Path) -> None:
    target = tmp_path / "sec.log"
    handler_id = logger.add(str(target), permissions=0o600, colorize=False)
    assert mode_of(target) == 0o600
    logger.remove(handler_id)


def test_permissions_survive_rotation(tmp_path: Path) -> None:
    target = tmp_path / "sec.log"
    handler_id = logger.add(
        str(target),
        format="{message}",
        colorize=False,
        rotation=1,
        permissions=0o600,
    )
    logger.info("one")
    logger.info("two")
    logger.remove(handler_id)

    assert mode_of(target) == 0o600
    rotated = [p for p in tmp_path.iterdir() if p.name != "sec.log"]
    assert rotated
    for old in rotated:
        assert mode_of(old) == 0o600


def test_permissions_rejects_non_file_sink() -> None:
    from io import StringIO

    with pytest.raises(ValueError, match="requires a file-path sink"):
        logger.add(StringIO(), permissions=0o600)


def test_permissions_rejects_bad_mode(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="permissions must be an int"):
        logger.add(str(tmp_path / "x.log"), permissions=0o1000)
