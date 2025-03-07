import asyncio
import pytest

from backend.api.users.auth.queries import delete_user
from backend.database.models.employer import EmployersOrm
from backend.database.models.worker import WorkersOrm
from backend.modules.redis.redis_utils import delete_object
from backend.schemas import EmployerResponseSchema, WorkerResponseSchema
from backend.tests.worker.utils_test import get_worker
from backend.tests.employer.utils_test import get_employer


async def delete_employer(employer):
    await delete_user(
        user_id=employer.id,
        user_table=EmployersOrm,
        response_schema=EmployerResponseSchema
    )
    await delete_object(obj_type='test_employer', obj_id=1)
    await delete_object(obj_type='test_employer_token', obj_id=1)
    await delete_object(obj_type='employer', obj_id=employer.id)

async def delete_worker(worker):
    await delete_user(
        user_id=worker.id,
        user_table=WorkersOrm,
        response_schema=WorkerResponseSchema
    )
    await delete_object(obj_type='test_worker', obj_id=1)
    await delete_object(obj_type='test_worker_token', obj_id=1)
    await delete_object(obj_type='worker', obj_id=worker.id)

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

