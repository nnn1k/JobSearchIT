from httpx import AsyncClient

from backend.api.users.auth.classes.AuthJWT import Token

from backend.utils.redis_utils import cache_object, get_cached_object
from backend.core.schemas import CompanySchema, EmployerResponseSchema, VacancySchema
from backend.tests.utils import base_url


async def employer_client():
    token = await get_cached_object(key='test_employer_token', schema=Token)
    return AsyncClient(
        base_url=base_url,
        cookies=token.model_dump(),
        timeout=10.0
    )


async def cache_employer(user=None, token=None):
    if user:
        await cache_object(
            key='test_employer',
            obj=user
        )
    if token:
        await cache_object(
            key='test_employer_token',
            obj=token
        )


async def get_employer():
    return await get_cached_object(
        key='test_employer',
        schema=EmployerResponseSchema
    )


async def cache_company(company):
    await cache_object(
        key='test_company',
        obj=company
    )


async def get_company():
    return await get_cached_object(
        key='test_company',
        schema=CompanySchema
    )


async def cache_vacancy(vacancy):
    await cache_object(
        key='test_vacancy',
        obj=vacancy
    )


async def get_vacancy():
    return await get_cached_object(
        key='test_vacancy',
        schema=VacancySchema
    )
