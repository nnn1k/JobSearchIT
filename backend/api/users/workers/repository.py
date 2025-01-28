from typing import Optional

from backend.database.utils.repository import AlchemyRepository
from backend.database.models.worker import WorkersOrm
from backend.api.users.workers.schemas import WorkerSchema, WorkerResponseSchema


class WorkerRepository(AlchemyRepository):
    db_model = WorkersOrm
    schema = WorkerSchema
    user_type = 'worker'


def get_worker_repo() -> WorkerRepository:
    return WorkerRepository()


async def get_worker_by_id(id: int) -> WorkerResponseSchema:
    worker_repo = get_worker_repo()
    worker = await worker_repo.get_one(id=id)
    worker_response = worker.model_dump(exclude='password')
    return WorkerResponseSchema.model_validate(worker_response, from_attributes=True)

