from fastapi import HTTPException, status, Cookie

from backend.api.users.auth.AuthJWT import jwt_token
from backend.api.users.employers.repository import get_employer_by_id
from backend.api.users.workers.repository import get_worker_by_id
from backend.schemas.global_schema import UserSchema

ACCESS_TOKEN = 'access_token'
REFRESH_TOKEN = 'refresh_token'


async def get_user_by_token_and_role(access_token, repository, schema):
    user = await check_user_role(access_token)

    if user.type != repository.user_type:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='bad user type',
        )
    user = await repository.get_one(id=int(user.id))
    if user:
        return schema.model_validate(user, from_attributes=True)


async def check_user_role(access_token=Cookie(None)) -> UserSchema:
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"not access token",
        )
    try:
        user_id = jwt_token.decode_jwt(token=access_token).get("sub")
        user_type = jwt_token.decode_jwt(token=access_token).get("type")
        return UserSchema(id=user_id, type=user_type)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token (access)",
        )

async def get_user_by_token(access_token=Cookie(None)):
    user = await check_user_role(access_token)
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
