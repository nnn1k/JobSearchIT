import asyncio
import pytest
from backend.tests.utils import delete_employer, delete_worker, get_employer, get_worker


async def clear_users():
    worker = await get_worker()
    if worker:
        await delete_worker(worker)

    employer = await get_employer()
    if employer:
        await delete_employer(employer)

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    asyncio.run(clear_users())
