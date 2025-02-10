from typing import Optional

from fastapi import Depends, Cookie

from backend.utils.auth_utils.token_dependencies import get_user_by_token_and_role
from backend.api.users.profile_dependencies import user_patch_dependencies
from backend.api.users.workers.profile.repository import get_worker_repo
from backend.api.users.workers.profile.schemas import WorkerSchema, WorkerProfileSchema, WorkerResponseSchema
from backend.schemas.global_schema import DynamicSchema
from backend.schemas.user_schema import UserSchema


async def get_worker_by_token(
    access_token=Cookie(None),
) -> UserSchema:
    worker_repo = get_worker_repo()
    return await get_user_by_token_and_role(access_token, worker_repo)


async def put_worker_dependencies(
        new_worker: WorkerProfileSchema,
        worker: WorkerSchema = Depends(get_worker_by_token)
) -> Optional[WorkerSchema]:
    worker_repo = get_worker_repo()
    return await worker_repo.update_one(id=worker.id, **new_worker.model_dump())

async def patch_worker_dependencies(
        new_worker: DynamicSchema,
        worker: WorkerSchema = Depends(get_worker_by_token)
) -> Optional[WorkerSchema]:
    worker_repo = get_worker_repo()
    return await user_patch_dependencies(worker, new_worker, worker_repo)
