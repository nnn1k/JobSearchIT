from typing import Any, Dict

from fastapi import HTTPException, status, Response

from backend.api.users.auth.classes.AuthJWT import Token, jwt_token
from backend.utils.auth_utils.check_func import exclude_password
from backend.api.users.auth.classes.HashPwd import HashPwd
from backend.utils.auth_utils.token_dependencies import ACCESS_TOKEN, REFRESH_TOKEN
from backend.utils.other.redis_func import get_code_from_redis
from backend.utils.other.type_utils import UserVar


async def register_user(user, repository) -> UserVar:
    if await repository.get_one(email=user.email):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user is exist",
        )
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="password mismatch",
        )
    new_user = await repository.add_one(
        email=user.email,
        password=HashPwd.hash_password(user.password),
    )
    return exclude_password(new_user, repository.response_schema)


async def login_user(user, repository) -> UserVar:
    new_user = await repository.get_one(email=user.email)
    if not new_user or not HashPwd.validate_password(password=user.password, hashed_password=new_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )
    return exclude_password(new_user, repository.response_schema)


async def check_user_code_dependencies(user, repository, code) -> UserVar:
    new_code = await get_code_from_redis(repository.user_type, user.id)
    if code.code == new_code:
        user = await repository.update_one(id=user.id, is_confirmed=True)
        return exclude_password(user, repository.response_schema)
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
