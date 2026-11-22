"""Smart logger wrapper with automatic default sink removal."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from loguru import logger as _loguru_logger

from logcraft.formatters.abbreviator import make_abbrev_patcher
from logcraft.sinks.archive_sink import make_archive_compression

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
        """
        if not self._default_removed:
            self._logger.remove()
            self._default_removed = True

        abbreviate = kwargs.pop("abbreviate", None)
        if abbreviate is not None:
            kwargs["format"] = self._wrap_format(kwargs.pop("format", None), abbreviate)

        archive_dir = kwargs.pop("archive_dir", None)
        if archive_dir is not None:
            if "compression" in kwargs:
                raise ValueError("archive_dir cannot be combined with explicit compression=")
            if not args or not isinstance(args[0], (str, Path)):
                raise ValueError("archive_dir requires a file-path sink")
            kwargs["compression"] = make_archive_compression(
                args[0],
                archive_dir,
                kwargs.pop("archive_compression", None),
            )
        else:
            kwargs.pop("archive_compression", None)

        return self._logger.add(*args, **kwargs)

    @staticmethod
    def _wrap_format(
        user_format: FormatTemplate,
        abbreviate: str,
    ) -> Callable[[dict[str, Any]], str]:
        """Build a dynamic format that abbreviates record['name'] per sink.

        Loguru has no per-sink patch hook, but a callable format receives the
        record before templating, so the record is mutated there. When a string
        template is converted to a callable, the exception field must be
        appended manually (loguru adds it automatically only for strings).
        """
        patcher = make_abbrev_patcher(abbreviate)

        if callable(user_format):
            inner: Callable[[dict[str, Any]], str] = user_format

            def from_callable(record: dict[str, Any]) -> str:
                patcher(record)
                return inner(record)

            return from_callable

        template = (user_format or DEFAULT_FORMAT) + "\n{exception}"

        def from_template(record: dict[str, Any]) -> str:
            patcher(record)
            return template

        return from_template

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
