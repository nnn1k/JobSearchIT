import redis.asyncio as async_redis
from fastapi import HTTPException, status


async def create_async_redis_client():
    connect_string = 'redis://default:MXnVzZUbxetVwLWVzvWSTLMIacVdknim@monorail.proxy.rlwy.net:44060'
    client = await async_redis.from_url(connect_string)
    return client


async def get_code_from_redis(user_type, user_id):
    redis_client = await create_async_redis_client()
    try:
        new_code = await redis_client.hget(f'{user_type}:{user_id}', 'code')
        new_code = new_code.decode('utf-8')
        return new_code
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Вышло время кода')


