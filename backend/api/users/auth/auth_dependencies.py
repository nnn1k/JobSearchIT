from typing import Literal, Any

from fastapi import HTTPException, status

from backend.api.users.employers.schemas import EmployerSchema
from backend.api.users.workers.schemas import WorkerSchema
from backend.utils.other.check_func import exclude_password
from backend.utils.other.hash_pwd import HashPwd
from backend.utils.other.redis_func import get_code_from_redis


async def register_user(user, repository) -> WorkerSchema or EmployerSchema:
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
    return new_user


async def login_user(user, repository) -> WorkerSchema or EmployerSchema:
    new_user = await repository.get_one(email=user.email)
    if not new_user or not HashPwd.validate_password(password=user.password, hashed_password=new_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )
    return exclude_password(new_user, repository.response_schema)


async def check_user_code_dependencies(user, repository, code) -> WorkerSchema or EmployerSchema:
    new_code = get_code_from_redis(repository.user_type, user.id)
    if code.code == new_code:
        return await repository.update_one(id=user.id, is_confirmed=True)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect code",
    )


async def send_code_response(email: str) -> dict[str, Any]:
    return {
        'message': 'Код отправлен на почту:',
        'email': email,
        'status': 'ok'
    }


async def confirm_email_response(email: str) -> dict[str, Any]:
    return {
        'message': 'Почта подтверждена',
        'email': email,
        'status': 'ok'
    }
