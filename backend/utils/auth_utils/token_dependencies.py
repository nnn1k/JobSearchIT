from fastapi import HTTPException, status, Cookie, Response

from backend.api.users.auth.classes.AuthJWT import jwt_token
from backend.api.users.employers.profile.queries import get_employer_by_id_queries

from backend.api.users.workers.profile.queries import get_worker_by_id_queries
from backend.schemas import EmployerResponseSchema
from backend.schemas import WorkerResponseSchema
from backend.schemas.user_schema import UserTypeSchema
from backend.utils.other.type_utils import UserVar

ACCESS_TOKEN = 'access_token'
REFRESH_TOKEN = 'refresh_token'


async def get_user_by_token_and_role(access_token=None, refresh_token=None, user_type=None, response=None) -> UserVar:
    user = await check_user_role(access_token, refresh_token, response)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token (access)",
        )
    if user.type != user_type:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='bad user type',
        )
    match user.type:
        case 'employer':
            return await get_employer_by_id_queries(user.id)
        case 'worker':
            return await get_worker_by_id_queries(user.id)
        case _:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='bad user type',
            )


async def check_user_role(access_token, refresh_token, response) -> UserTypeSchema | None:
    if access_token is None:
        return check_refresh_token(refresh_token, response)
    try:
        user_id = jwt_token.decode_jwt(token=access_token).get("sub")
        user_type = jwt_token.decode_jwt(token=access_token).get("type")
        return UserTypeSchema(id=user_id, type=user_type)
    except Exception:
        return check_refresh_token(refresh_token, response)


def check_refresh_token(refresh_token, response):
    if refresh_token is None:
        return None
    try:
        new_access_token, new_refresh_token = jwt_token.token_refresh(refresh_token)
        if new_access_token is None or new_refresh_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token (refresh)",
            )

        response.set_cookie(key=ACCESS_TOKEN, value=new_access_token)
        response.set_cookie(key=REFRESH_TOKEN, value=new_refresh_token)
        user_id = jwt_token.decode_jwt(token=new_access_token).get("sub")
        user_type = jwt_token.decode_jwt(token=new_access_token).get("type")
        return UserTypeSchema(id=user_id, type=user_type)
    except Exception:
        return None


async def get_user_by_token(access_token=Cookie(None), refresh_token=Cookie(None), response: Response = None) -> None | WorkerResponseSchema | EmployerResponseSchema:
    user = await check_user_role(access_token, refresh_token, response)
    if not user:
        return None
    match user.type:
        case 'worker':
            return await get_worker_by_id_queries(user.id)
        case 'employer':
            return await get_employer_by_id_queries(user.id)
        case _:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"invalid user type",
            )
