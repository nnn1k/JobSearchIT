from fastapi import Cookie, HTTPException
from starlette import status
from starlette.responses import Response

from backend.api.users.employers.profile.queries import get_employer_by_id_queries
from backend.api.users.workers.profile.queries import get_worker_by_id_queries

from backend.schemas import EmployerResponseSchema, WorkerResponseSchema
from backend.utils.auth_utils.token_dependencies import check_user_role, get_user_by_token_and_role


async def get_employer_by_token(
        response: Response,
        access_token=Cookie(None),
        refresh_token=Cookie(None),
) -> EmployerResponseSchema:
    return await get_user_by_token_and_role(access_token, refresh_token, 'employer', response)


async def get_worker_by_token(
        response: Response,
        access_token=Cookie(None),
        refresh_token=Cookie(None),
) -> WorkerResponseSchema:
    return await get_user_by_token_and_role(access_token=access_token, refresh_token=refresh_token, user_type='worker', response=response)


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
