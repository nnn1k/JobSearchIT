from fastapi import HTTPException
from starlette import status

from backend.core.utils.redis_utils.redis_obj_utils import create_async_redis_client


async def get_code_from_redis(user_type, user_id) -> str:
    redis_client = await create_async_redis_client()
    try:
        new_code = await redis_client.hget(f'{user_type}_code:{user_id}', 'code')
        new_code = new_code.decode('utf-8')
        return new_code
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Вышло время кода')


async def add_code_to_redis(user, code, ttl=1500):
    redis_client = await create_async_redis_client()
    await redis_client.hset(f'{user.type}_code:{user.id}', mapping={'code': code, 'email': user.email})
    await redis_client.expire(f'{user.type}_code:{user.id}', ttl)
