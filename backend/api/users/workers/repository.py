from backend.database.utils.repository import AlchemyRepository
from backend.database.models.worker import WorkersOrm
from backend.api.users.workers.schemas import WorkerSchema


class WorkerRepository(AlchemyRepository):
    db_model = WorkersOrm
    schema = WorkerSchema
    user_type = 'worker'


def get_worker_repo():
    return WorkerRepository()


async def get_worker_by_id(id: int):
    repo = get_worker_repo()
    return await repo.get_one(id=id)

