import redis
from fastapi import HTTPException, status


def create_redis_client():
    connect_string = 'redis://default:MXnVzZUbxetVwLWVzvWSTLMIacVdknim@monorail.proxy.rlwy.net:44060'
    client = redis.from_url(connect_string)
    return client

def get_code_from_redis(user_type, user_id):
    redis_client = create_redis_client()
    try:
        new_code = redis_client.hget(f'{user_type}:{user_id}', 'code').decode('utf-8')
    except Exception as e:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Вышло время кода')
    return new_code

