from httpx import AsyncClient

from backend.api.users.auth.classes.AuthJWT import Token
from backend.api.users.auth.queries import delete_user
from backend.database.models.worker import WorkersOrm
from backend.modules.redis.redis_utils import cache_object, delete_object, get_cached_object
from backend.schemas import ResumeSchema, WorkerResponseSchema
from backend.tests.utils import base_url


async def worker_client():
    token = await get_cached_object(obj_id=1, obj_type='test_worker_token', schema=Token)
    return AsyncClient(
        base_url=base_url,
        cookies=token.model_dump(),
        timeout=10.0
    )


async def cache_worker(user=None, token=None):
    if user:
        await cache_object(
            obj_id=1,
            obj_type='test_worker',
            obj=user
        )
    if token:
        await cache_object(
            obj_id=1,
            obj_type='test_worker_token',
            obj=token
        )


async def get_worker():
    return await get_cached_object(
        obj_id=1,
        obj_type='test_worker',
        schema=WorkerResponseSchema
    )


async def delete_worker(worker):
    await delete_user(
        user_id=worker.id,
        user_table=WorkersOrm,
        response_schema=WorkerResponseSchema
    )
    await delete_object(obj_type='test_worker', obj_id=1)
    await delete_object(obj_type='test_worker_token', obj_id=1)
    await delete_object(obj_type='worker', obj_id=worker.id)


async def cache_resume(resume):
    await cache_object(
        obj_id=1,
        obj_type='test_resume',
        obj=resume
    )

async def get_resume():
    return await get_cached_object(
        obj_id=1,
        obj_type='test_resume',
        schema=ResumeSchema
    )

