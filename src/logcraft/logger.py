"""Smart logger wrapper with automatic default sink removal."""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from loguru import logger as _loguru_logger

from logcraft.formatters.abbreviator import make_abbrev_patcher
from logcraft.sinks.archive_sink import make_archive_compression
from logcraft.sinks.permissions import chmod_if_exists, validate_mode

DEFAULT_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

FormatTemplate = Callable[[dict[str, Any]], str] | str | None


class SmartLogger:
    """Wrapper over loguru.logger.

    The first add() call removes the default stderr sink that Loguru creates
    on import (the root cause of duplicated lines in terminals).
    Everything else is delegated to the underlying loguru logger.
    """

    def __init__(self) -> None:
        self._logger = _loguru_logger
        self._default_removed = False

    def add(self, *args: Any, **kwargs: Any) -> int:
        """Add a sink; removes the default stderr sink on the first call.

        Extra kwargs (not present in loguru):
            abbreviate: module-name abbreviation style
                        ("initials" | "last" | "last2").
            archive_dir: directory where rotated log files are moved.
            archive_compression: "gz" | "bz2" | "xz" | "zip" | None.
            permissions: file mode for the log file, e.g. 0o600.
        """
        if not self._default_removed:
            self._logger.remove()
            self._default_removed = True

        abbreviate = kwargs.pop("abbreviate", None)

        archive_dir = kwargs.pop("archive_dir", None)
        if archive_dir is not None:
            if "compression" in kwargs:
                raise ValueError("archive_dir cannot be combined with explicit compression=")
            if not args or not isinstance(args[0], (str, Path)):
                raise ValueError("archive_dir requires a file-path sink")
            kwargs["compression"] = make_archive_compression(
                args[0], archive_dir, kwargs.pop("archive_compression", None)
            )
        else:
            kwargs.pop("archive_compression", None)

        permissions = kwargs.pop("permissions", None)
        perm_path: Path | None = None
        perm_state: dict[str, Any] | None = None
        if permissions is not None:
            validate_mode(permissions)
            if not args or not isinstance(args[0], (str, Path)):
                raise ValueError("permissions requires a file-path sink")
            perm_path = Path(args[0])
            perm_state = {"ino": None}

        if abbreviate is not None or perm_state is not None:
            kwargs["format"] = self._build_format(
                kwargs.pop("format", None),
                abbreviate,
                perm_path,
                perm_state,
                permissions,
            )

        handler_id = self._logger.add(*args, **kwargs)

        if perm_path is not None and permissions is not None:
            chmod_if_exists(perm_path, permissions)

        return handler_id

    @staticmethod
    def _build_format(
        user_format: FormatTemplate,
        abbreviate: str | None,
        perm_path: Path | None,
        perm_state: dict[str, Any] | None,
        perm_mode: int | None,
    ) -> Callable[[dict[str, Any]], str]:
        """Build a dynamic format applying per-sink record transformations.

        Loguru has no per-sink patch hook, but a callable format receives the
        record before templating, so the record is mutated there. The same hook
        re-applies file permissions after each rotation (detected via inode).
        When a string template is converted to a callable, the exception field
        must be appended manually (loguru adds it automatically for strings).
        """
        patcher = make_abbrev_patcher(abbreviate) if abbreviate is not None else None

        def apply_perms() -> None:
            if perm_path is None or perm_state is None or perm_mode is None:
                return
            try:
                st = perm_path.stat()
            except OSError:
                return
            if perm_state.get("ino") != st.st_ino:
                os.chmod(perm_path, perm_mode)
                perm_state["ino"] = st.st_ino

        if callable(user_format):
            inner: Callable[[dict[str, Any]], str] = user_format

            def dynamic_callable(record: dict[str, Any]) -> str:
                if patcher is not None:
                    patcher(record)
                if perm_state is not None:
                    apply_perms()
                return inner(record)

            return dynamic_callable

        template = (user_format or DEFAULT_FORMAT) + "\n{exception}"

        def dynamic_template(record: dict[str, Any]) -> str:
            if patcher is not None:
                patcher(record)
            if perm_state is not None:
                apply_perms()
            return template

        return dynamic_template

    def remove(self, handler_id: int | None = None) -> None:
        """Remove a sink by id, or all sinks at once."""
        self._logger.remove(handler_id)
        if handler_id is None:
            self._default_removed = True

    def bind(self, **kwargs: Any) -> SmartLogger:
        """Contextual logger with bound extra fields."""
        bound = SmartLogger()
        bound._logger = self._logger.bind(**kwargs)
        bound._default_removed = self._default_removed
        return bound

    def __getattr__(self, name: str) -> Any:
        """Delegate everything else (success, trace, patch, catch, opt, ...)."""
        return getattr(self._logger, name)


logger = SmartLogger()
