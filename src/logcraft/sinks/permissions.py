"""File permissions control for log files (Loguru issue #401)."""

from __future__ import annotations

import os
from pathlib import Path

MIN_MODE = 0o000
MAX_MODE = 0o777


def validate_mode(mode: int) -> None:
    """Raise ValueError if mode is not a valid permission mask."""
    if not isinstance(mode, int) or not MIN_MODE <= mode <= MAX_MODE:
        raise ValueError(f"permissions must be an int in 0o000..0o777, got {mode!r}")


def chmod_if_exists(path: str | Path, mode: int) -> None:
    """Apply mode to path if the file already exists."""
    p = Path(path)
    if p.exists():
        os.chmod(p, mode)
