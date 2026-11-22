"""Tests for HTMLSink."""

from pathlib import Path

from logcraft import logger
from logcraft.sinks import HTMLSink


def test_html_sink_streams_colored_page(tmp_path: Path, capsys) -> None:
    path = tmp_path / "logs.html"
    sink = HTMLSink(path)
    handler_id = logger.add(
        sink,
        format="<blue>{time:HH:mm:ss}</blue> | <level>{level: <8}</level> | <level>{message}</level>",
        colorize=True,
    )

    logger.info("plain info")
    logger.error('boom & "quotes"')

    logger.remove(handler_id)  # вызывает sink.stop()

    content = path.read_text(encoding="utf-8")
    captured = capsys.readouterr()

    assert content.startswith("<!DOCTYPE html>")
    assert "plain info" in content
    assert "boom" in content
    assert "<span style=" in content   # цвета на месте
    assert "\x1b" not in content       # ANSI-мусора нет
    assert captured.out == ""          # ничего не_echo в stdout
    assert captured.err == ""          # ничего не_echo в stderr


def test_html_sink_appends_to_existing_page(tmp_path: Path) -> None:
    path = tmp_path / "logs.html"
    for message in ("first", "second"):
        sink = HTMLSink(path)
        handler_id = logger.add(sink, format="<level>{message}</level>", colorize=True)
        logger.info(message)
        logger.remove(handler_id)

    content = path.read_text(encoding="utf-8")
    assert content.count("<!DOCTYPE html>") == 1
    assert "first" in content
    assert "second" in content