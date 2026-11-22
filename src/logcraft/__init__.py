"""LogCraft: Loguru-based logging with Rich rendering and profiling."""

from logcraft._version import __version__
from logcraft.logger import logger
from logcraft.sinks import HTMLSink, RichSink

__all__ = ["HTMLSink", "RichSink", "__version__", "logger"]
