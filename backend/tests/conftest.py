import asyncio
import pytest

from backend.api.companies.queries import delete_company_queries
from backend.api.users.auth.queries import delete_user
from backend.core.database.models.employer import EmployersOrm
from backend.core.database.models.worker import WorkersOrm
from backend.core.utils.redis_utils.redis_obj_utils import delete_object
from backend.core.schemas import EmployerResponseSchema, WorkerResponseSchema
from backend.tests.worker.utils_test import get_worker
from backend.tests.employer.utils_test import get_company, get_employer


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
    company = await get_company()
    if employer:
        await delete_company_queries(company_id=company.id, owner=employer)
        await delete_employer(employer)


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    asyncio.run(clear_users())

