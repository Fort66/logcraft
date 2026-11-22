"""Tests for SmartLogger."""

import sys
from io import StringIO

from logcraft import logger


def test_auto_remove_default_sink():
    """Test that default sink is automatically removed on first add()."""
    # Capture stderr to verify no duplicate output
    old_stderr = sys.stderr
    sys.stderr = StringIO()

    try:
        # Add a sink to stdout
        output = StringIO()
        handler_id = logger.add(output, format="{message}")

        # Log a message
        logger.info("Test message")

        # Check that message appears only once (in our sink, not in stderr)
        output.seek(0)
        assert output.read().strip() == "Test message"

        # Stderr should be empty (no duplicate from default sink)
        sys.stderr.seek(0)
        assert sys.stderr.read() == ""

        # Cleanup
        logger.remove(handler_id)
    finally:
        sys.stderr = old_stderr


def test_logging_levels():
    """Test all logging levels."""
    output = StringIO()
    handler_id = logger.add(output, format="{level} | {message}")

    try:
        logger.debug("debug msg")
        logger.info("info msg")
        logger.warning("warning msg")
        logger.error("error msg")
        logger.critical("critical msg")

        output.seek(0)
        lines = output.read().strip().split("\n")

        assert len(lines) == 5
        assert "DEBUG | debug msg" in lines[0]
        assert "INFO | info msg" in lines[1]
        assert "WARNING | warning msg" in lines[2]
        assert "ERROR | error msg" in lines[3]
        assert "CRITICAL | critical msg" in lines[4]
    finally:
        logger.remove(handler_id)


def test_bind_context():
    """Test binding contextual data."""
    output = StringIO()
    handler_id = logger.add(output, format="{extra[user]} | {message}")

    try:
        context_logger = logger.bind(user="alice")
        context_logger.info("User action")

        output.seek(0)
        assert output.read().strip() == "alice | User action"
    finally:
        logger.remove(handler_id)


def test_exception_logging():
    """Test exception logging with traceback."""
    output = StringIO()
    handler_id = logger.add(output, format="{message}")

    try:
        try:
            raise ValueError("Test error")
        except ValueError:
            logger.exception("An error occurred")

        output.seek(0)
        content = output.read()

        assert "An error occurred" in content
        assert "ValueError" in content
        assert "Test error" in content
    finally:
        logger.remove(handler_id)
