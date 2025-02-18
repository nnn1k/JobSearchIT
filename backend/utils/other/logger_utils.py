import os

from loguru import logger

log_directory = os.path.join(os.getcwd(), "backend/logs")
info_log_path = os.path.join(log_directory, "info.log")
debug_log_path = os.path.join(log_directory, "debug.log")
error_log_path = os.path.join(log_directory, "error.log")
os.makedirs(log_directory, exist_ok=True)

logger.add(
    info_log_path,
    level="INFO",
)

logger.add(
    debug_log_path,
    level="DEBUG",
)

logger.add(
    error_log_path,
    level="ERROR",
)

