import json
from typing import Dict

import redis

from backend.core.utils.other.time_utils import time_it_async
from backend.core.utils.other.type_utils import BaseVar
from backend.core.utils.settings import settings

TTL = 600


async def create_async_redis_client():
    redis_client = await redis.asyncio.from_url(settings.redis.url)
    return redis_client


async def clear_redis():
    redis_client = await create_async_redis_client()
    await redis_client.flushdb()


@time_it_async
async def check_redis_connection():
    redis_client = await create_async_redis_client()
    await redis_client.ping()


async def cache_object(key: str, obj: BaseVar, ttl=TTL) -> None:
    redis_client = await create_async_redis_client()
    await redis_client.set(key, obj.model_dump_json(), ex=ttl)


async def get_cached_object(key: str, schema: BaseVar = None) -> BaseVar | Dict | None:
    redis_client = await create_async_redis_client()
    obj_json = await redis_client.get(key)
    if obj_json:
        decoded_obj = json.loads(obj_json.decode('utf-8'))
        if schema:
            return schema.model_validate(decoded_obj, from_attributes=True)
        return dict(decoded_obj)
    return None


async def delete_object(obj_type: str, obj_id: int):
    redis_client = await create_async_redis_client()
    await redis_client.delete(f'{obj_type}_obj:{obj_id}')
