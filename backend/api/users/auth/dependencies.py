from typing import Any, Dict

from fastapi import HTTPException, status, Response
from starlette import status

from backend.api.users.auth.classes.AuthJWT import Token, jwt_token
from backend.api.users.auth.classes.HashPwd import HashPwd
from backend.api.users.auth.queries import login_user_queries, register_user_queries, update_code_queries
from backend.api.users.auth.schemas import UserType
from backend.database.models.employer import EmployersOrm
from backend.database.models.worker import WorkersOrm
from backend.schemas import EmployerResponseSchema, WorkerResponseSchema
from backend.utils.auth_utils.token_dependencies import ACCESS_TOKEN, REFRESH_TOKEN
from backend.utils.other.redis_func import get_code_from_redis
from backend.utils.other.type_utils import UserVar


def get_login_db_model(user_type: UserType):
    match user_type:
        case UserType.employer:
            return EmployersOrm, EmployerResponseSchema
        case UserType.worker:
            return WorkersOrm, WorkerResponseSchema
        case _:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")


async def register_user(user, db_model, response_schema) -> UserVar:
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="password mismatch",
        )
    new_user = await register_user_queries(user, db_model, response_schema)
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user is exist",
        )
    return new_user


async def login_user(user, db_model, response_schema) -> UserVar:
    new_user = await login_user_queries(user, db_model, response_schema)
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )
    return new_user


async def check_user_code_dependencies(user, user_type, db_model, response_schema, code) -> UserVar:
    new_code = await get_code_from_redis(user_type, user.id)
    if code.code == new_code:
        return await update_code_queries(user.id, db_model, response_schema)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect code",
    )


def create_token(response: Response, user) -> Dict[str, Any]:
    access_token = jwt_token.create_access_token(id=user.id, user_type=user.type)
    refresh_token = jwt_token.create_refresh_token(id=user.id, user_type=user.type)

    response.set_cookie(ACCESS_TOKEN, access_token)
    response.set_cookie(REFRESH_TOKEN, refresh_token)
    response.set_cookie('user_type', user.type)
    token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    return {
        'user': user,
        'token': token,
        'status': 'ok'
    }
