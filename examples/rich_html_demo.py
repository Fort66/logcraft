"""RichSink for terminal + HTMLSink for colored log pages."""

from logcraft import logger
from logcraft.sinks import HTMLSink, RichSink

TERMINAL_FORMAT = (
    "<cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan> | "
    "<level>{level: <8}</level> | "
    "<magenta>{name}</magenta>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)
HTML_FORMAT = (
    "<blue>{time:YYYY-MM-DD HH:mm:ss}</blue> | "
    "<level>{level: <8}</level> | "
    "<level>{message}</level>"
)

logger.remove()

logger.add(
    RichSink(),
    format=TERMINAL_FORMAT,
    colorize=True,
    backtrace=True,
    diagnose=True,
)
logger.add(
    HTMLSink("app_logs.html"),
    format=HTML_FORMAT,
    colorize=True,
    backtrace=True,
    diagnose=True,
)


def risky_math(a: int, b: int) -> float:
    step1 = a + b
    step2 = step1 / b
    return step2


logger.info("Application started successfully")
logger.warning("This is a warning")

try:
    risky_math(5, 0)
except ZeroDivisionError:
    logger.exception("An error occurred during division")

logger.info("Open app_logs.html in a browser to see the colored log page")