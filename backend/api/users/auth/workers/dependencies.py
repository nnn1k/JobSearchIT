from fastapi import Depends

from backend.api.users.auth.auth_dependencies import register_user, login_user, check_user_code_dependencies
from backend.api.users.workers.repository import get_worker_repo
from backend.schemas.global_schema import CodeSchema
from backend.api.users.workers.schemas import WorkerRegisterSchema, WorkerAuthSchema, WorkerSchema
from backend.utils.other.email_func import SendEmail
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
    SendEmail.send_code_to_email(worker, 'worker')
    return worker

async def check_code_dependencies(
        code: CodeSchema,
        worker: WorkerSchema = Depends(get_worker_by_token),
):
    worker_repo = get_worker_repo()
    return await check_user_code_dependencies(worker, worker_repo, code)
