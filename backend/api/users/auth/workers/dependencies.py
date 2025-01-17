from fastapi import HTTPException, status

from backend.api.users.workers.repository import get_worker_repo
from backend.schemas.worker_schemas import WorkerRegisterSchema, WorkerAuthSchema, WorkerSchema
from backend.utils.hash_pwd import HashPwd

async def login_worker(
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

async def register_worker(
        reg_worker: WorkerRegisterSchema,
) -> WorkerSchema:
    worker_repo = get_worker_repo()
    if await worker_repo.get_one(email=reg_worker.email):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
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
