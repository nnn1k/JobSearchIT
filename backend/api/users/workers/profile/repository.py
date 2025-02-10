from typing import List

from backend.api.skills.schemas import SkillSchema
from backend.database.utils.repository import AlchemyRepository
from backend.database.models.worker.Worker import WorkersOrm
from backend.api.users.workers.profile.schemas import WorkerResponseSchema, WorkerSchema
from backend.utils.auth_utils.check_func import exclude_password


class WorkerRepository(AlchemyRepository):
    db_model = WorkersOrm
    schema = WorkerSchema
    response_schema = WorkerResponseSchema
    user_type = 'worker'


def get_worker_repo() -> WorkerRepository:
    return WorkerRepository()


async def get_worker_by_id(id: int) -> WorkerResponseSchema:
    worker_repo = get_worker_repo()
    worker = await worker_repo.get_one(id=id)
    return exclude_password(worker, WorkerResponseSchema)


class WorkerResponseSchemaWithRel(WorkerResponseSchema):
    skills: List[SkillSchema] = []


async def get_worker_by_id_rel(id: int):
    worker_repo = get_worker_repo()
    worker = await worker_repo.get_one_rel(id=id, load=[{'type': 'selectin', 'relationship': 'skills'}])
    return worker
