from backend.api.v1.users.auth.schemas import WorkerSchema, EmployerSchema
from backend.core.schemas import WorkerResponseSchema, EmployerResponseSchema
from backend.core.services.users.repository import UserRepository


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

    async def get_worker_rel(self, **kwargs) -> WorkerResponseSchema:
        worker = await self.user_repo.get_worker_rel(**kwargs)
        schema = WorkerResponseSchema.model_validate(worker)
        return schema

    async def get_employer_rel(self, **kwargs) -> EmployerResponseSchema:
        employer = await self.user_repo.get_employer_rel(**kwargs)
        schema = EmployerResponseSchema.model_validate(employer)
        return schema

    async def update_worker(self, worker: WorkerSchema, **kwargs) -> WorkerSchema:
        worker = await self.user_repo.update_worker(id=worker.id, **kwargs)
        schema = WorkerSchema.model_validate(worker)
        return schema

    async def update_employer(self, employer: EmployerSchema, **kwargs) -> EmployerSchema:
        employer = await self.user_repo.update_employer(id=employer.id, **kwargs)
        schema = EmployerSchema.model_validate(employer)
        return schema

