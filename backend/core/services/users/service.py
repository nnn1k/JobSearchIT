from backend.core.schemas.models.employer.employer_schema import EmployerSchema
from backend.core.schemas import WorkerSchemaRel, EmployerSchemaRel, WorkerSchema
from backend.core.services.users.repository import UserRepository
from backend.core.utils.exc import employer_not_found_exc, worker_not_found_exc


class UserService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_worker_by_id(self, id: int) -> WorkerSchema:
        worker = await self.user_repo.get_worker(id=id)
        schema = WorkerSchema.model_validate(worker)
        return schema

    async def get_employer_by_id(self, id: int) -> EmployerSchema:
        employer = await self.user_repo.get_employer(id=id)
        schema = EmployerSchema.model_validate(employer)
        return schema

    async def get_worker_rel(self, **kwargs) -> WorkerSchemaRel:
        worker = await self.user_repo.get_worker_rel(**kwargs)
        schema = WorkerSchemaRel.model_validate(worker)
        return schema

    async def get_employer_rel(self, **kwargs) -> EmployerSchemaRel:
        employer = await self.user_repo.get_employer_rel(**kwargs)
        schema = EmployerSchemaRel.model_validate(employer)
        return schema

    async def update_worker(self, worker_id: int, **kwargs) -> WorkerSchema:
        worker = await self.user_repo.update_worker(id=worker_id, **kwargs)
        if not worker:
            raise worker_not_found_exc
        schema = WorkerSchema.model_validate(worker)
        return schema

    async def update_employer(self, employer_id: int, **kwargs) -> EmployerSchema:
        employer = await self.user_repo.update_employer(id=employer_id, **kwargs)
        if not employer:
            raise employer_not_found_exc
        schema = EmployerSchema.model_validate(employer)
        return schema

