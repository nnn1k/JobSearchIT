from fastapi import Depends, Cookie

from backend.api.users.auth.token_dependencies import get_user_by_token_and_role
from backend.api.users.profile_dependencies import patch_dependencies
from backend.api.users.workers.repository import get_worker_repo
from backend.api.users.workers.schemas import WorkerSchema, WorkerProfileSchema, WorkerUpdateSchema


async def get_worker_by_token(
    access_token=Cookie(None),
) -> WorkerSchema:
    worker_repo = get_worker_repo()
    return await get_user_by_token_and_role(access_token, worker_repo, WorkerSchema)


async def put_worker_dependencies(
        new_worker: WorkerProfileSchema,
        worker: WorkerSchema = Depends(get_worker_by_token)
):
    worker_repo = get_worker_repo()
    return await worker_repo.update_one(id=worker.id, **new_worker.model_dump())

async def patch_worker_dependencies(
        new_worker: WorkerUpdateSchema,
        worker: WorkerSchema = Depends(get_worker_by_token)
):
    worker_repo = get_worker_repo()
    return await patch_dependencies(worker, new_worker, worker_repo)
