"""Rich terminal sink — renders Loguru's ANSI stream through the Rich engine."""

from __future__ import annotations

import sys
from typing import IO

from rich.console import Console
from rich.text import Text


class RichSink:
    """
    Терминальный sink. Loguru генерирует ANSI-коды (colorize=True),
    Rich рендерит их: TrueColor, жирный, курсив, корректный перенос.
    Пишет в stderr, как это делает сам Loguru по умолчанию.
    """

    def __init__(
        self,
        file: IO[str] | None = None,
        *,
        width: int | None = None,
        force_terminal: bool | None = None,
    ) -> None:
        self.console = Console(
            file=file if file is not None else sys.stderr,
            width=width,
            highlight=False,
            soft_wrap=True,
            force_terminal=force_terminal,
        )

    def write(self, message: str) -> None:
        self.console.print(Text.from_ansi(message), end="")

    def stop(self) -> None:
        pass