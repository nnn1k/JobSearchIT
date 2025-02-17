import json
from typing import List

import redis.asyncio as async_redis
from fastapi import HTTPException, status

from backend.utils.other.celery_utils import cl_app
from backend.utils.other.type_utils import BaseVar

from backend.utils.other.logger_utils import logger


async def create_async_redis_client():
    connect_string = 'redis://default:MXnVzZUbxetVwLWVzvWSTLMIacVdknim@monorail.proxy.rlwy.net:44060'
    client = await async_redis.from_url(connect_string)
    return client


async def get_code_from_redis(user_type, user_id):
    redis_client = await create_async_redis_client()
    try:
        new_code = await redis_client.hget(f'{user_type}_code:{user_id}', 'code')
        new_code = new_code.decode('utf-8')
        return new_code
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Вышло время кода')


async def add_code_to_redis(user, code):
    redis_client = await create_async_redis_client()
    await redis_client.hset(f'{user.type}_code:{user.id}', mapping={'code': code, 'email': user.email})
    await redis_client.expire(f'{user.type}_code:{user.id}', 1500)


@cl_app.task
async def cache_object(obj: BaseVar, obj_id: int = 0, obj_type: str = '', ttl=1):
    if obj_id == 0:
        obj_id = obj.id
    if obj_type == '':
        obj_type = obj.type
    redis_client = await create_async_redis_client()
    await redis_client.set(f'{obj_type}_obj:{obj_id}', obj.model_dump_json(), ex=ttl)


@cl_app.task
async def cache_list_object(objects: List[BaseVar], ttl=1):
    redis_client = await create_async_redis_client()
    for obj in objects:
        await redis_client.set(f'{obj.type}_obj:{obj.id}', obj.model_dump_json(), ex=ttl)


@cl_app.task
async def get_cached_object(obj_type: str, obj_id: int, schema: BaseVar = None):
    redis_client = await create_async_redis_client()
    obj_json = await redis_client.get(f'{obj_type}_obj:{obj_id}')
    if obj_json:
        decoded_obj = json.loads(obj_json.decode('utf-8'))
        if schema:
            return schema.model_validate(decoded_obj, from_attributes=True)
        return dict(decoded_obj)
    return None


@cl_app.task
async def delete_object(obj_type: str, obj_id: int):
    redis_client = await create_async_redis_client()
    await redis_client.delete(f'{obj_type}_obj:{obj_id}')


@cl_app.task
async def refresh_objects(obj_dict: dict) -> None:
    from backend.utils.str_const import (
        WORKER_USER_TYPE,
        EMPLOYER_USER_TYPE,
        VACANCY_TYPE,
        RESUME_TYPE,
        COMPANY_TYPE
    )
    from backend.api.users.employers.profile.queries import get_employer_by_id_queries
    from backend.api.users.workers.profile.queries import get_worker_by_id_queries
    from backend.api.vacancies.queries import get_vacancy_by_id_queries
    from backend.api.companies.queries import get_company_by_id_queries
    from backend.api.users.workers.resumes.queries import get_one_resume_by_id_queries
    query_mapping = {
        WORKER_USER_TYPE: get_worker_by_id_queries,
        EMPLOYER_USER_TYPE: get_employer_by_id_queries,
        VACANCY_TYPE: get_vacancy_by_id_queries,
        RESUME_TYPE: get_one_resume_by_id_queries,
        COMPANY_TYPE: get_company_by_id_queries,
    }
    for key, value in obj_dict.items():
        logger.info(f'key: {key}, value: {value}')
        query_function = query_mapping.get(key)
        query_function.delay(value, refresh=True)
