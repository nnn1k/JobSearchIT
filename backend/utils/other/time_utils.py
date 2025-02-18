import time
from datetime import datetime, timedelta
from functools import wraps
import inspect
from .logger_utils import logger


def current_time():
    return datetime.utcnow() + timedelta(hours=3)


def time_it_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time

        frame = inspect.currentframe().f_back
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno

        if 'backend' in filename:
            filename = filename.split('backend', 1)[-1]
        else:
            filename = filename

        logger.debug(f"Функция {func.__name__} выполнена за {duration:.4f} секунд. "
              f"Вызвана из {filename}, строка {lineno}.")
        return result

    return wrapper
