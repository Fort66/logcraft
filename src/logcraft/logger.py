"""Smart logger wrapper with automatic default sink removal."""

from typing import Any

from loguru import logger as _loguru_logger


class SmartLogger:
    """
    Обёртка над loguru.logger.

    Главное отличие: первый вызов add() автоматически убирает дефолтный
    stderr-sink, который Loguru создаёт при импорте (причина дублей в терминале).
    Все прочие методы loguru доступны через делегирование.
    """

    def __init__(self) -> None:
        self._logger = _loguru_logger
        self._default_removed = False

    def add(self, *args: Any, **kwargs: Any) -> int:
        """Добавить sink; при первом вызове убирает дефолтный stderr-sink."""
        if not self._default_removed:
            self._logger.remove()
            self._default_removed = True
        return self._logger.add(*args, **kwargs)

    def remove(self, handler_id: int | None = None) -> None:
        """Убрать sink по id или все сразу."""
        self._logger.remove(handler_id)
        if handler_id is None:
            self._default_removed = True

    def bind(self, **kwargs: Any) -> "SmartLogger":
        """Контекстный logger с привязанными extra-полями."""
        bound = SmartLogger()
        bound._logger = self._logger.bind(**kwargs)
        bound._default_removed = self._default_removed
        return bound

    def __getattr__(self, name: str) -> Any:
        """Делегирует всё остальное (success, trace, patch, catch, opt, ...)."""
        return getattr(self._logger, name)


logger = SmartLogger()