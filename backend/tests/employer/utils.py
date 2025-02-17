from httpx import AsyncClient

from backend.api.users.auth.classes.AuthJWT import Token
from backend.api.users.auth.queries import delete_user
from backend.database.models.employer import EmployersOrm
from backend.modules.redis.redis_utils import cache_object, delete_object, get_cached_object
from backend.schemas import CompanySchema, EmployerResponseSchema, VacancySchema
from backend.tests.utils import base_url



async def employer_client():
    token = await get_cached_object(obj_id=1, obj_type='test_employer_token', schema=Token)
    return AsyncClient(
        base_url=base_url,
        cookies=token.model_dump(),
        timeout=10.0
    )


async def get_employer():
    return await get_cached_object(
        obj_id=1,
        obj_type='test_employer',
        schema=EmployerResponseSchema
    )


async def delete_employer(employer):
    await delete_user(
        user_id=employer.id,
        user_table=EmployersOrm,
        response_schema=EmployerResponseSchema
    )
    await delete_object(obj_type='test_employer', obj_id=1)
    await delete_object(obj_type='test_employer_token', obj_id=1)
    await delete_object(obj_type='employer', obj_id=employer.id)


async def cache_employer(user=None, token=None):
    if user:
        await cache_object(
            obj_id=1,
            obj_type='test_employer',
            obj=user
        )
    if token:
        await cache_object(
            obj_id=1,
            obj_type='test_employer_token',
            obj=token
        )

async def cache_company(company):
    await cache_object(
        obj_id=1,
        obj_type='test_company',
        obj=company
    )

async def get_company():
    return await get_cached_object(
        obj_id=1,
        obj_type='test_company',
        schema=CompanySchema
    )

async def cache_vacancy(vacancy):
    await cache_object(
        obj_id=1,
        obj_type='test_vacancy',
        obj=vacancy
    )

async def get_vacancy():
    return await get_cached_object(
        obj_id=1,
        obj_type='test_vacancy',
        schema=VacancySchema
    )
