from typing import Optional

from fastapi import Cookie, HTTPException, status, Response


from backend.api.users.employers.profile.queries import get_employer_by_id_queries
from backend.api.users.workers.profile.queries import get_worker_by_id_queries

from backend.schemas import EmployerResponseSchema, WorkerResponseSchema
from backend.utils.auth_utils.token_dependencies import check_user_role
from backend.utils.str_const import EMPLOYER_USER_TYPE, WORKER_USER_TYPE

from backend.utils.other.logger_utils import logger


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
        user_type: Optional[str] = None
) -> None | WorkerResponseSchema | EmployerResponseSchema:
    user_jwt_schema = await check_user_role(access_token, refresh_token, response)
    if not user_jwt_schema:
        if user_type is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token (access)",
            )
        return None
    logger.info(f'user_type: {user_type}, user_jwt_schema: {user_jwt_schema}')
    if user_type:
        if user_jwt_schema.type != user_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"invalid user type",
            )
    if user_jwt_schema.type == WORKER_USER_TYPE:
        return await get_worker_by_id_queries(user_jwt_schema.id)
    if user_jwt_schema.type == EMPLOYER_USER_TYPE:
        return await get_employer_by_id_queries(user_jwt_schema.id)


