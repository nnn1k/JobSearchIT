import os

from loguru import logger

log_directory = os.path.join(os.getcwd(), "backend/logs")

info_log_path = os.path.join(log_directory, "info.log")
time_log_path = os.path.join(log_directory, "time.log")
error_log_path = os.path.join(log_directory, "error.log")
db_log_path = os.path.join(log_directory, "database.log")

logger.level('DATABASE', no=25, color='<cyan>')
logger.level('TIME', no=26, color='<yellow>')

os.makedirs(log_directory, exist_ok=True)

logger.add(
    db_log_path,
    level="DATABASE"
)

logger.add(
    time_log_path,
    level="TIME",
)

logger.add(
    info_log_path,
    level="INFO",
)

logger.add(
    error_log_path,
    level="ERROR",
)


