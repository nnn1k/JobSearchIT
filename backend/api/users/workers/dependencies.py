from fastapi import Depends, HTTPException, status

from backend.api.users.auth.token_dependencies import get_worker_by_token
from backend.api.users.workers.repository import get_worker_repo
from backend.api.users.workers.schemas import WorkerSchema, WorkerProfileSchema, WorkerUpdateSchema


async def update_worker_dependencies(
        new_worker: WorkerProfileSchema,
        worker: WorkerSchema = Depends(get_worker_by_token)
):
    worker_repo = get_worker_repo()
    return await worker_repo.update_one(id=worker.id, **new_worker.model_dump())

async def new_update_worker_dependencies(
        new_worker: WorkerUpdateSchema,
        worker: WorkerSchema = Depends(get_worker_by_token)
):
    worker_repo = get_worker_repo()
    keys = worker.__fields__.keys()
    if new_worker.key not in keys:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Key {new_worker.key} not found."
        )
    if new_worker.key in ('password', 'created_at', 'updated_at', 'id'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Key {new_worker.key} is immutable"
        )
    update_data = {new_worker.key: new_worker.value}
    return await worker_repo.update_one(id=worker.id, **update_data)