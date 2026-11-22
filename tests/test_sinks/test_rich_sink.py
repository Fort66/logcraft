"""Tests for RichSink."""

import io

from logcraft import logger
from logcraft.sinks import RichSink


def test_rich_sink_strips_styles_for_non_tty() -> None:
    buffer = io.StringIO()
    handler_id = logger.add(
        RichSink(file=buffer),
        format="<level>{level}</level> | <level>{message}</level>",
        colorize=True,
    )
    logger.info("hello rich")
    logger.remove(handler_id)

    output = buffer.getvalue()
    assert "hello rich" in output
    assert "\x1b" not in output


def test_rich_sink_keeps_ansi_for_terminal() -> None:
    buffer = io.StringIO()
    sink = RichSink(file=buffer, force_terminal=True)
    handler_id = logger.add(sink, format="<green>{message}</green>", colorize=True)
    logger.info("colored")
    logger.remove(handler_id)

    output = buffer.getvalue()
    assert "colored" in output
    assert "\x1b[" in output
