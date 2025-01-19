from fastapi import HTTPException, status, Depends

from backend.api.users.workers.repository import get_worker_repo
from backend.schemas.global_schema import CodeSchema
from backend.api.users.workers.schemas import WorkerRegisterSchema, WorkerAuthSchema, WorkerSchema
from backend.utils.email_func import send_code_to_email
from backend.utils.hash_pwd import HashPwd
from backend.utils.redis_func import get_code_from_redis
from backend.api.users.auth.token_dependencies import get_worker_by_token


async def login_worker_dependencies(
    log_user: WorkerAuthSchema
) -> WorkerSchema:
    worker_repo = get_worker_repo()
    worker = await worker_repo.get_one(email=log_user.email)
    if not worker or not HashPwd.validate_password(password=log_user.password, hashed_password=worker.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )
    return worker

async def register_worker_dependencies(
        reg_worker: WorkerRegisterSchema,
) -> WorkerSchema:
    worker_repo = get_worker_repo()
    if await worker_repo.get_one(email=reg_worker.email):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user is exist",
        )
    if reg_worker.password != reg_worker.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="password mismatch",
        )
    worker = await worker_repo.add_one(
        email=reg_worker.email,
        password=HashPwd.hash_password(reg_worker.password),
    )
    return worker

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
