"""Custom sinks for LogCraft."""

from logcraft.sinks.archive_sink import make_archive_compression
from logcraft.sinks.html_sink import HTMLSink
from logcraft.sinks.rich_sink import RichSink

__all__ = ["HTMLSink", "RichSink", "make_archive_compression"]
