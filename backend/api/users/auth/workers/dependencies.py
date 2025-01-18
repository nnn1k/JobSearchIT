from fastapi import HTTPException, status, Depends

from backend.api.users.workers.repository import get_worker_repo
from backend.schemas.worker_schemas import WorkerRegisterSchema, WorkerAuthSchema, WorkerSchema
from backend.utils.email_func import SendEmail
from backend.utils.hash_pwd import HashPwd
from backend.utils.redis_func import create_redis_client
from backend.api.users.auth.token_dependencies import get_worker_by_token


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

async def get_code(
        worker: WorkerSchema = Depends(get_worker_by_token),
):
    code = SendEmail.get_random_code()
    message = f'Ваш код {code}'
    redis_client = create_redis_client()
    redis_client.hset(f'user:{worker.id}', 'code', code)
    SendEmail.post_mail(worker.email, message)
    return worker

async def check_code(
        code: str,
        worker: WorkerSchema = Depends(get_worker_by_token),
):
    redis_client = create_redis_client()
    new_code = redis_client.hget(f'user:{worker.id}', 'code').decode('utf-8')
    if code == new_code:
        worker_repo = get_worker_repo()
        return await worker_repo.update_one(id=worker.id, is_confirmed=True)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect code",
    )
