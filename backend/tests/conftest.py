import asyncio
import pytest
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.database import session_factory
from backend.core.database.models.employer import EmployersOrm, CompaniesOrm
from backend.core.database.models.worker import WorkersOrm
from backend.core.utils.exc import user_is_not_owner_exc, company_not_found_exc, employer_not_found_exc
from backend.core.utils.redis_utils.redis_obj_utils import delete_object
from backend.core.schemas import EmployerSchemaRel, WorkerSchemaRel
from backend.tests.worker.utils_test import get_worker
from backend.tests.employer.utils_test import get_company, get_employer


async def delete_user(user_id: int, user_table, response_schema):
    async with session_factory() as session:
        stmt = await session.execute(
            delete(user_table)
            .filter_by(id=user_id)
            .returning(user_table)
        )
        deleted_user = stmt.scalars().one_or_none()
        if deleted_user:
            schema = response_schema.model_validate(deleted_user, from_attributes=True)
            await session.commit()
            return schema
        return None


async def delete_employer(employer):
    await delete_user(
        user_id=employer.id,
        user_table=EmployersOrm,
        response_schema=EmployerSchemaRel
    )
    await delete_object(obj_type='test_employer', obj_id=1)
    await delete_object(obj_type='test_employer_token', obj_id=1)
    await delete_object(obj_type='employer', obj_id=employer.id)


async def delete_worker(worker):
    await delete_user(
        user_id=worker.id,
        user_table=WorkersOrm,
        response_schema=WorkerSchemaRel
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


async def delete_company_queries(company_id: int, owner: EmployerSchemaRel, session: AsyncSession = None):
    if not session:
        session = session_factory()
    if not (company_id == owner.company_id and owner.is_owner):
        raise user_is_not_owner_exc

    stmt = await session.execute(
        delete(CompaniesOrm)
        .filter_by(id=company_id)
        .returning(CompaniesOrm)
    )
    company = stmt.scalars().one_or_none()
    if not company:
        raise company_not_found_exc
    stmt = await session.execute(
        update(EmployersOrm)
        .values(company_id=None, is_owner=False)
        .filter_by(id=owner.id)
    )
    employer = stmt.scalars().one_or_none()
    if not employer:
        raise employer_not_found_exc
    await session.commit()
