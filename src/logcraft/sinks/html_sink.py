"""Streaming HTML sink: Loguru ANSI -> colored HTML log page, line by line."""

from __future__ import annotations

import html
from pathlib import Path
from typing import IO

from rich.ansi import AnsiDecoder
from rich.console import Console
from rich.text import Text

_PAGE_HEADER = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>LogCraft Logs</title>
<style>
  body {{ background: {bg}; color: {fg}; margin: 0; padding: 16px; }}
  .line {{ font-family: Consolas, Monaco, "Courier New", monospace;
           font-size: 13px; line-height: 1.45;
           white-space: pre-wrap; word-break: break-word; }}
</style>
</head>
<body>
"""


class HTMLSink:
    """
    Пишет логи в HTML-страницу потоково: каждая строка — сразу в файл.
    Цвета берёт из ANSI-кодов Loguru через Rich (AnsiDecoder + Style.get_html_style),
    поэтому в файле нет мусора вида \\x1b[31m, а при краше процесса уже записанное
    не теряется (в отличие от буферизованного export_html).
    """

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._decoder = AnsiDecoder()
        self._console = Console()  # только для резолва стилей, ничего не печатает
        is_new = not self._path.exists() or self._path.stat().st_size == 0
        self._file: IO[str] = self._path.open("a", encoding="utf-8")
        if is_new:
            self._file.write(_PAGE_HEADER.format(bg="#1e1e1e", fg="#d4d4d4"))
        self._closed = False

    def write(self, message: str) -> None:
        if self._closed:
            return
        lines = message.split("\n")
        if lines and lines[-1] == "":
            lines.pop()
        for line in lines:
            self._file.write(f'<div class="line">{self._line_to_html(line)}</div>\n')
        self._file.flush()

    def stop(self) -> None:
        if not self._closed:
            self._file.flush()
            self._file.close()
            self._closed = True

    def _line_to_html(self, line: str) -> str:
        text: Text = self._decoder.decode_line(line)
        plain = text.plain
        if not text.spans:
            return html.escape(plain)
        out: list[str] = []
        pos = 0
        for span in sorted(text.spans, key=lambda s: (s.start, s.end)):
            if span.start < pos:  # защита от перекрывающихся span
                continue
            if span.start > pos:
                out.append(html.escape(plain[pos:span.start]))
            css = self._console.get_style(span.style).get_html_style()
            chunk = html.escape(plain[span.start:span.end])
            out.append(f'<span style="{css}">{chunk}</span>' if css else chunk)
            pos = span.end
        out.append(html.escape(plain[pos:]))
        return "".join(out)
