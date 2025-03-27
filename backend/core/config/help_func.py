import asyncio
import sys
from asyncio import WindowsSelectorEventLoopPolicy


def check_platform():
    # Установка политики цикла событий
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
