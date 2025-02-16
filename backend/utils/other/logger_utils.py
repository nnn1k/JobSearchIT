import os

from loguru import logger

log_directory = "/backend/logs"
os.makedirs(log_directory, exist_ok=True)

logger.add(
    os.path.join(log_directory, "logging.log"),
    level="DEBUG",
    rotation="10 MB",
    retention="1 days",
)

