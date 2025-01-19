from backend.database.utils.repository import AlchemyRepository
from backend.database.models.worker import WorkersOrm
from backend.api.users.workers.schemas import WorkerSchema


class WorkerRepository(AlchemyRepository):
    db_model = WorkersOrm
    schema = WorkerSchema
    user_type = 'worker'

def get_worker_repo():
    return WorkerRepository()

