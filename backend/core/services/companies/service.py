from typing import Sequence

from backend.core.schemas.models.employer.employer_schema import EmployerSchema
from backend.core.schemas.models.employer.company_schema import CompanySchemaRel, CompanySchema, CompanyAddSchema
from backend.core.schemas.models.other.review_schema import ReviewCreate, ReviewSchema, ReviewSchemaRel
from backend.core.schemas.models.worker.worker_schema import WorkerSchema
from backend.core.services.companies.repository import CompanyRepository
from backend.core.services.users.service import UserService
from backend.core.utils.exc import company_not_found_exc, user_is_not_owner_exc, user_have_company_exc, \
    review_not_found_exc, user_have_review_exc


class CompanyService:
    def __init__(self, company_repo: CompanyRepository, user_serv: UserService):
        self.company_repo = company_repo
        self.user_serv = user_serv

    async def create_company(self, new_company: CompanyAddSchema, employer: EmployerSchema) -> CompanySchema:
        if employer.company_id:
            raise user_have_company_exc
        new_company = await self.company_repo.create_company(name=new_company.name, description=new_company.description)
        schema = CompanySchema.model_validate(new_company)
        await self.user_serv.update_employer(employer_id=employer.id, company_id=new_company.id, is_owner=True)
        return schema

    async def get_company(self, company_id: int) -> CompanySchema:
        company = await self.company_repo.get_company(id=company_id)
        if not company:
            raise company_not_found_exc
        schema = CompanySchema.model_validate(company)
        return schema

    async def get_company_rel(self, company_id: int) -> CompanySchemaRel:
        company = await self.company_repo.get_company_rel(id=company_id)
        if not company:
            raise company_not_found_exc
        schema = CompanySchemaRel.model_validate(company)
        return schema

    async def update_company(self, company_id: int, employer: EmployerSchema, **kwargs) -> CompanySchema:
        if employer.company_id != company_id or not employer.is_owner:
            raise user_is_not_owner_exc
        new_company = await self.company_repo.update_company(id=company_id, **kwargs)
        if not new_company:
            raise company_not_found_exc
        schema = CompanySchema.model_validate(new_company)
        return schema

    async def delete_company(self, company_id: int, employer: EmployerSchema) -> None:
        if not (company_id == employer.company_id and employer.is_owner):
            raise user_is_not_owner_exc
        await self.user_serv.update_employer(employer_id=employer.id, company_id=None, is_owner=False)
        company = await self.company_repo.delete_company(id=company_id)
        if not company:
            raise company_not_found_exc

    async def add_review(self, worker: WorkerSchema, company_id: int, new_review: ReviewCreate) -> ReviewSchema:
        company = await self.get_company(company_id=company_id)
        if not company:
            raise company_not_found_exc
        old_review = await self.company_repo.get_review(worker_id=worker.id)
        if old_review:
            raise user_have_review_exc
        new_review = await self.company_repo.add_review(
            worker_id=worker.id, company_id=company_id, score=new_review.score, message=new_review.message
        )
        schema = ReviewSchema.model_validate(new_review)
        return schema

    async def get_review(self, review_id: int, company_id: int) -> ReviewSchemaRel:
        company = await self.get_company(company_id=company_id)
        if not company:
            raise company_not_found_exc
        review = await self.company_repo.get_review(id=review_id)
        if not review:
            raise review_not_found_exc
        schema = ReviewSchemaRel.model_validate(review)
        return schema

    async def get_reviews(self, company_id: int) -> Sequence[ReviewSchemaRel]:
        company = await self.get_company(company_id=company_id)
        if not company:
            raise company_not_found_exc
        reviews = await self.company_repo.get_reviews(company_id=company_id)
        return [ReviewSchemaRel.model_validate(rev) for rev in reviews]

    async def update_review(
            self, worker: WorkerSchema, review_id: int, company_id: int, new_review: ReviewCreate
    ) -> ReviewSchema:
        company = await self.get_company(company_id=company_id)
        if not company:
            raise company_not_found_exc
        new_review = await self.company_repo.update_review(
            review_id=review_id, score=new_review.score, message=new_review.message
        )
        if not new_review:
            raise review_not_found_exc
        schema = ReviewSchema.model_validate(new_review)
        if schema.worker_id != worker.id:
            raise user_is_not_owner_exc
        return schema

    async def delete_review(self, worker: WorkerSchema, company_id: int, review_id: int) -> ReviewSchema:
        company = await self.get_company(company_id=company_id)
        if not company:
            raise company_not_found_exc
        review = await self.company_repo.delete_review(review_id=review_id)
        schema = ReviewSchema.model_validate(review)
        if schema.worker_id != worker.id:
            raise user_is_not_owner_exc
        return schema
