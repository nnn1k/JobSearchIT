import asyncio
import sys


def check_platform():
    # Установка политики цикла событий
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
