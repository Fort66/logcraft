"""Basic usage example of LogCraft."""

from logcraft import logger

# SmartLogger сам уберёт дефолтный stderr-sink при первом add()
logger.add("app.log", rotation="10 MB", retention="1 week")

logger.info("Application started")
logger.debug("Debug information")
logger.warning("This is a warning")

# Контекстное логирование
user_logger = logger.bind(user="alice", request_id="12345")
user_logger.info("User performed action")

# Обработка исключений
try:
    result = 10 / 0
except ZeroDivisionError:
    logger.exception("Division by zero occurred")

logger.info("Application finished")