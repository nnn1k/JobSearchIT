from fastapi import Depends

from backend.api.users.auth.token_dependencies import get_worker_by_token
from backend.api.users.workers.repository import get_worker_repo
from backend.api.users.workers.schemas import WorkerSchema, WorkerProfileSchema


async def update_worker_dependencies(
        new_worker: WorkerProfileSchema,
        worker: WorkerSchema = Depends(get_worker_by_token)
):
    worker_repo = get_worker_repo()
    return await worker_repo.update_one(id=worker.id, **new_worker.model_dump())
