from typing import Optional

from fastapi import Cookie, Depends, HTTPException, Query, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.users.employers.profile.queries import get_employer_by_id_queries
from backend.api.users.workers.profile.queries import get_worker_by_id_queries
from backend.database.utils.dependencies import get_db

from backend.schemas import EmployerResponseSchema, WorkerResponseSchema
from backend.utils.auth_utils.token_dependencies import check_user_role
from backend.utils.const import EMPLOYER_USER_TYPE, WORKER_USER_TYPE

from backend.utils.other.logger_utils import logger


async def get_employer_by_token(
        response: Response,
        access_token=Cookie(None),
        refresh_token=Cookie(None),
        session: AsyncSession = Depends(get_db),
) -> EmployerResponseSchema:
    return await get_user_by_token(
        access_token=access_token,
        refresh_token=refresh_token,
        response=response,
        user_type=EMPLOYER_USER_TYPE,
        session=session,
    )


async def get_worker_by_token(
        response: Response,
        access_token=Cookie(None),
        refresh_token=Cookie(None),
        session: AsyncSession = Depends(get_db),
) -> WorkerResponseSchema:
    return await get_user_by_token(
        access_token=access_token,
        refresh_token=refresh_token,
        response=response,
        user_type=WORKER_USER_TYPE,
        session=session,
    )


async def get_user_by_token(
        access_token=Cookie(None, include_in_schema=False),
        refresh_token=Cookie(None, include_in_schema=False),
        response: Response = None,
        user_type: Optional[str] = Query(None, include_in_schema=False),
        session: AsyncSession = Depends(get_db),
) -> None | WorkerResponseSchema | EmployerResponseSchema:
    user_jwt_schema = await check_user_role(access_token, refresh_token, response)
    if not user_jwt_schema:
        if user_type is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token (access)",
            )
        return None
    if user_type:
        if user_jwt_schema.type != user_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"invalid user type",
            )
    if user_jwt_schema.type == WORKER_USER_TYPE:
        return await get_worker_by_id_queries(user_jwt_schema.id, session)
    if user_jwt_schema.type == EMPLOYER_USER_TYPE:
        return await get_employer_by_id_queries(user_jwt_schema.id, session)
