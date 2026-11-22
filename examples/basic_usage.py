"""Basic usage example of LogCraft."""

from logcraft import logger

# No need to call logger.remove() - it's automatic!
logger.add("app.log", rotation="10 MB", retention="1 week")

logger.info("Application started")
logger.debug("Debug information")
logger.warning("This is a warning")

# Contextual logging
user_logger = logger.bind(user="alice", request_id="12345")
user_logger.info("User performed action")

# Exception handling
try:
    result = 10 / 0
except ZeroDivisionError:
    logger.exception("Division by zero occurred")

logger.info("Application finished")