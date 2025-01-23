from fastapi import HTTPException, status, Depends, Cookie, Response

from backend.api.users.auth.AuthJWT import jwt_token
from backend.api.users.auth.auth_dependencies import register_user, login_user
from backend.api.users.workers.repository import get_worker_repo
from backend.schemas.global_schema import CodeSchema
from backend.api.users.workers.schemas import WorkerRegisterSchema, WorkerAuthSchema, WorkerSchema
from backend.utils.other.email_func import send_code_to_email
from backend.utils.other.redis_func import get_code_from_redis
from backend.api.users.auth.token_dependencies import ACCESS_TOKEN, REFRESH_TOKEN
from backend.api.users.workers.dependencies import get_worker_by_token


async def login_worker_dependencies(
    log_user: WorkerAuthSchema
) -> WorkerSchema:
    worker_repo = get_worker_repo()
    return await login_user(log_user, worker_repo)

async def register_worker_dependencies(
        reg_user: WorkerRegisterSchema,
) -> WorkerSchema:
    worker_repo = get_worker_repo()
    return await register_user(reg_user, worker_repo)

async def get_code_dependencies(
        worker: WorkerSchema = Depends(get_worker_by_token),
):
    send_code_to_email(worker, 'worker')
    return worker

async def check_code_dependencies(
        code: CodeSchema,
        worker: WorkerSchema = Depends(get_worker_by_token),
):
    new_code = get_code_from_redis('worker', worker.id)
    if code.code == new_code:
        worker_repo = get_worker_repo()
        return await worker_repo.update_one(id=worker.id, is_confirmed=True)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect code",
    )

def refresh_token_dependencies(
        response: Response,
        refresh_token=Cookie(None)
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no refresh token",
        )
    new_access_token, new_refresh_token = jwt_token.token_refresh(refresh_token)
    if new_access_token is None or new_refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token (refresh)",
        )
    response.set_cookie(key=ACCESS_TOKEN, value=new_access_token)
    response.set_cookie(key=REFRESH_TOKEN, value=new_refresh_token)
    return response
