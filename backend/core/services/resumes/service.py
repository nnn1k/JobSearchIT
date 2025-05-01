from sqlalchemy.exc import IntegrityError

from backend.api.v1.resumes.schemas import ResumeAddSchema, ResumeUpdateSchema
from backend.core.schemas import WorkerSchema, ResumeSchema, ResumeSchemaRel
from backend.core.services.resumes.repository import ResumeRepository
from backend.core.utils.exc import user_have_this_profession_exc, resume_not_found_exc, user_is_not_owner_exc


class ResumeService:

    def __init__(self, resume_repo: ResumeRepository):
        self.resume_repo = resume_repo

    async def create_resume(self, new_resume: ResumeAddSchema, worker: WorkerSchema) -> ResumeSchema:
        try:
            resume = await self.resume_repo.create_resume(
                profession_id=new_resume.profession_id,
                salary_first=new_resume.salary_first,
                salary_second=new_resume.salary_second,
                description=new_resume.description,
                city=new_resume.city,
                worker_id=worker.id,
            )
        except IntegrityError:
            raise user_have_this_profession_exc
        schema = ResumeSchema.model_validate(resume)
        return schema

    async def get_resume(self, resume_id: int) -> ResumeSchema:
        resume = await self.resume_repo.get_resume(id=resume_id)
        if not resume:
            raise resume_not_found_exc
        schema = ResumeSchema.model_validate(resume)
        return schema

    async def get_resume_rel(self, resume_id: int) -> ResumeSchemaRel:
        resume = await self.resume_repo.get_resume_rel(id=resume_id)
        if not resume:
            raise resume_not_found_exc
        schema = ResumeSchemaRel.model_validate(resume)
        return schema

    async def update_resume(self, resume_id: int, worker: WorkerSchema, new_resume: ResumeUpdateSchema) -> ResumeSchema:
        try:
            resume = await self.resume_repo.update_resume(
                resume_id=resume_id,
                profession_id=new_resume.profession_id,
                salary_first=new_resume.salary_first,
                salary_second=new_resume.salary_second,
                description=new_resume.description,
                city=new_resume.city,
            )
        except IntegrityError:
            raise user_have_this_profession_exc
        if not resume:
            raise resume_not_found_exc
        if resume.worker_id != worker.id:
            raise user_is_not_owner_exc
        schema = ResumeSchema.model_validate(resume)
        return schema

    async def delete_resume(self, resume_id: int, worker: WorkerSchema) -> None:
        resume = await self.resume_repo.delete_resume(resume_id=resume_id)
        if not resume:
            raise resume_not_found_exc
        if not (worker.id == resume.worker_id):
            raise user_is_not_owner_exc

