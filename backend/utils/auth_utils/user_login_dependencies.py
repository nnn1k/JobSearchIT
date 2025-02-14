from fastapi import Cookie, HTTPException
from starlette import status
from starlette.responses import Response

from backend.api.users.employers.profile.queries import get_employer_by_id_queries
from backend.api.users.workers.profile.queries import get_worker_by_id_queries

from backend.schemas import EmployerResponseSchema, WorkerResponseSchema
from backend.utils.auth_utils.token_dependencies import check_user_role
from backend.utils.str_const import EMPLOYER_USER_TYPE, WORKER_USER_TYPE


async def get_employer_by_token(
        response: Response,
        access_token=Cookie(None),
        refresh_token=Cookie(None),
) -> EmployerResponseSchema:
    return await get_user_by_token(
        access_token=access_token,
        refresh_token=refresh_token,
        response=response,
        user_type=EMPLOYER_USER_TYPE
    )


async def get_worker_by_token(
        response: Response,
        access_token=Cookie(None),
        refresh_token=Cookie(None),
) -> WorkerResponseSchema:
    return await get_user_by_token(
        access_token=access_token,
        refresh_token=refresh_token,
        response=response,
        user_type=WORKER_USER_TYPE
    )


async def get_user_by_token(
        access_token=Cookie(None),
        refresh_token=Cookie(None),
        response: Response = None,
        user_type=None
) -> None | WorkerResponseSchema | EmployerResponseSchema:
    user_jwt_schema = await check_user_role(access_token, refresh_token, response)
    if user_jwt_schema is None:
        if user_type is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token (access)",
            )
        return None
    if user_type == WORKER_USER_TYPE:
        return await get_worker_by_id_queries(user_jwt_schema.id)
    if user_type == EMPLOYER_USER_TYPE:
        return await get_employer_by_id_queries(user_jwt_schema.id)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid user type",
    )
