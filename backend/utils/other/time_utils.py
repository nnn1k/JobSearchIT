import time
from datetime import datetime, timedelta
from functools import wraps
import inspect
from .logger_utils import logger
from pyinstrument import Profiler


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

        logger.log('TIME', f"Функция {func.__name__} выполнена за {duration:.4f} секунд. \n"
                           f"Вызвана из {filename}, строка {lineno}. \n")
        return result

    return wrapper


def profile_pyinstrument(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Создаем профилировщик
        profiler = Profiler()
        profiler.start()

        # Выполняем функцию
        result = func(*args, **kwargs)

        # Останавливаем профилировщик
        profiler.stop()

        # Выводим результаты
        print(profiler.output_text(unicode=True, color=True))
        profiler.reset()
        return result

    return wrapper
