from backend.database.utils.repository import AlchemyRepository
from backend.database.models.worker import WorkersOrm
from backend.schemas.worker_schemas import WorkerSchema


class WorkerRepository(AlchemyRepository):
    db_model = WorkersOrm
    schema = WorkerSchema

def get_worker_repo():
    return WorkerRepository()

