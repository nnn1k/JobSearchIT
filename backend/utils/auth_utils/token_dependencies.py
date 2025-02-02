from fastapi import HTTPException, status, Cookie

from backend.utils.auth_utils.AuthJWT import jwt_token
from backend.api.users.employers.repository import get_employer_by_id
from backend.api.users.employers.schemas import EmployerSchema
from backend.api.users.workers.profile.repository import get_worker_by_id
from backend.api.users.workers.profile.schemas import WorkerSchema
from backend.schemas.global_schema import UserTypeSchema, UserSchema
from backend.utils.auth_utils.check_func import exclude_password

ACCESS_TOKEN = 'access_token'
REFRESH_TOKEN = 'refresh_token'


async def get_user_by_token_and_role(access_token, repository, schema, response_schema) -> UserSchema:
    user = await check_user_role(access_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token (access)",
        )
    if user.type != repository.user_type:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='bad user type',
        )
    user = await repository.get_one(id=int(user.id))
    if user:
        return exclude_password(user, response_schema)


async def check_user_role(access_token=Cookie(None)) -> UserTypeSchema | None:
    if access_token is None:
        return None
    try:
        user_id = jwt_token.decode_jwt(token=access_token).get("sub")
        user_type = jwt_token.decode_jwt(token=access_token).get("type")
        return UserTypeSchema(id=user_id, type=user_type)
    except Exception:
        return None


async def get_user_by_token(access_token=Cookie(None)) -> WorkerSchema or EmployerSchema or None:
    user = await check_user_role(access_token)
    if not user:
        return None
    match user.type:
        case 'worker':
            return await get_worker_by_id(user.id)
        case 'employer':
            return await get_employer_by_id(user.id)
        case _:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"invalid user type",
            )
