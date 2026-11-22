"""Smart logger wrapper with automatic default sink removal."""

from loguru import logger as _loguru_logger
from typing import Any


class SmartLogger:
    """
    Smart wrapper around loguru.logger that automatically removes
    the default stderr sink on first add() call.

    Usage:
        from logcraft import logger

        # No need to call logger.remove() manually
        logger.add("app.log", rotation="10 MB")
        logger.info("Application started")
    """

    def __init__(self):
        self._default_removed = False
        self._logger = _loguru_logger

    def add(self, *args: Any, **kwargs: Any) -> int:
        """
        Add a sink to the logger.

        Automatically removes the default stderr sink on first call.

        Args:
            *args: Positional arguments passed to loguru.logger.add()
            **kwargs: Keyword arguments passed to loguru.logger.add()

        Returns:
            int: Handler ID that can be used to remove the sink later
        """
        if not self._default_removed:
            self._logger.remove()
            self._default_removed = True

        return self._logger.add(*args, **kwargs)

    def remove(self, handler_id: int | None = None) -> None:
        """
        Remove a sink from the logger.

        Args:
            handler_id: Handler ID returned by add(). If None, removes all sinks.
        """
        self._logger.remove(handler_id)

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message."""
        self._logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message."""
        self._logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message."""
        self._logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message."""
        self._logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a critical message."""
        self._logger.critical(message, *args, **kwargs)

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an exception with traceback."""
        self._logger.exception(message, *args, **kwargs)

    def bind(self, **kwargs: Any) -> "SmartLogger":
        """
        Bind contextual data to the logger.

        Args:
            **kwargs: Key-value pairs to bind

        Returns:
            SmartLogger: New logger instance with bound context
        """
        new_logger = SmartLogger()
        new_logger._logger = self._logger.bind(**kwargs)
        new_logger._default_removed = self._default_removed
        return new_logger

    def opt(self, **kwargs: Any) -> Any:
        """
        Configure logger options.

        Args:
            **kwargs: Options like exception=True, colors=True, etc.

        Returns:
            Logger with configured options
        """
        return self._logger.opt(**kwargs)

    def level(self, name: str, no: int | None = None, color: str | None = None, 
              icon: str | None = None) -> Any:
        """
        Get or create a custom log level.

        Args:
            name: Level name
            no: Level number (if creating)
            color: Color markup (if creating)
            icon: Icon (if creating)

        Returns:
            Level object
        """
        return self._logger.level(name, no=no, color=color, icon=icon)

    def configure(self, **kwargs: Any) -> None:
        """
        Configure the logger with multiple handlers and extra context.

        Args:
            **kwargs: Configuration dict with 'handlers' and 'extra' keys
        """
        # Remove default sink before configuring
        if not self._default_removed:
            self._logger.remove()
            self._default_removed = True

        self._logger.configure(**kwargs)


# Global logger instance
logger = SmartLogger()