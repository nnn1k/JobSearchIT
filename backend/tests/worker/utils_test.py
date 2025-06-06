from httpx import AsyncClient

from backend.api.v1.users.auth.classes.AuthJWT import Token

from backend.core.utils.redis_utils.redis_obj_utils import cache_object, get_cached_object
from backend.core.schemas import ResumeSchema, WorkerSchemaRel
from backend.tests.utils import base_url


async def worker_client():
    token = await get_cached_object(key='test_worker_token', schema=Token)
    return AsyncClient(
        base_url=base_url,
        cookies=token.model_dump(),
        timeout=10.0
    )


async def cache_worker(user=None, token=None):
    if user:
        await cache_object(
            key='test_worker',
            obj=user,
            ttl=1_000_000
        )
    if token:
        await cache_object(
            key='test_worker_token',
            obj=token,
            ttl=1_000_000
        )


async def get_worker():
    return await get_cached_object(
        key='test_worker',
        schema=WorkerSchemaRel
    )


async def cache_resume(resume):
    await cache_object(
        key='test_resume',
        obj=resume,
        ttl=1_000_000
    )


async def get_resume():
    return await get_cached_object(
        key='test_resume',
        schema=ResumeSchema
    )
