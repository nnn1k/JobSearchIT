from typing import Optional

from fastapi import Depends, Cookie

from backend.api.users.workers.profile.queries import update_worker_by_id_queries
from backend.utils.auth_utils.token_dependencies import get_user_by_token_and_role
from backend.api.users.workers.profile.schemas import WorkerProfileSchema
from backend.schemas import WorkerResponseSchema
from backend.schemas.global_schema import DynamicSchema


async def get_worker_by_token(
    access_token=Cookie(None),
) -> WorkerResponseSchema:
    return await get_user_by_token_and_role(access_token, 'worker')


async def put_worker_dependencies(
        new_worker: WorkerProfileSchema,
        worker: WorkerResponseSchema = Depends(get_worker_by_token)
) -> Optional[WorkerResponseSchema]:
    return await update_worker_by_id_queries(worker_id=worker.id, **new_worker.model_dump())

async def patch_worker_dependencies(
        new_worker: DynamicSchema,
        worker: WorkerResponseSchema = Depends(get_worker_by_token)
) -> Optional[WorkerResponseSchema]:
    return await update_worker_by_id_queries(worker_id=worker.id, **new_worker.model_dump())
