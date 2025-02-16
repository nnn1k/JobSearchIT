from httpx import AsyncClient
from backend.api.users.auth.classes.AuthJWT import Token
from backend.api.users.auth.queries import delete_user
from backend.database.models.employer import EmployersOrm
from backend.database.models.worker import WorkersOrm
from backend.modules.redis.redis_utils import cache_object, delete_object, get_cached_object
from backend.schemas import EmployerResponseSchema, WorkerResponseSchema
from backend.schemas.user_schema import UserResponseSchema

base_url = 'http://127.0.0.1:8000/api/'

test_user = {
    "email": "testtest@example.com",
    "password": "string",
    "confirm_password": "string"
}


def async_client():
    return AsyncClient(
        base_url=base_url,
        timeout=10.0
    )


async def worker_client():
    token = await get_cached_object(obj_id=1, obj_type='test_worker_token', schema=Token)
    return AsyncClient(
        base_url=base_url,
        cookies=token.model_dump(),
        timeout=10.0
    )


async def employer_client():
    token = await get_cached_object(obj_id=1, obj_type='test_employer_token', schema=Token)
    return AsyncClient(
        base_url=base_url,
        cookies=token.model_dump(),
        timeout=10.0
    )


def check_user(response):
    user = response.json().get('user')
    user_schema = UserResponseSchema.model_validate(user, from_attributes=True)
    assert user is not None
    assert isinstance(user_schema, UserResponseSchema)
    return user_schema


def check_token(response):
    token = response.json().get('token')
    token_schema = Token.model_validate(token, from_attributes=True)
    assert token is not None
    assert isinstance(token_schema, Token)
    return token_schema


async def cache_worker(user, token):
    await cache_object(
        obj_id=1,
        obj_type='test_worker',
        obj=user
    )
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
