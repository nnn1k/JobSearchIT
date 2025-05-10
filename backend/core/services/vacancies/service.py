from typing import List, Sequence

from sqlalchemy.exc import IntegrityError

from backend.api.v1.skills.queries import update_vacancy_skills
from backend.core.schemas import VacancySchema, EmployerSchema, SkillSchema
from backend.core.schemas.models.employer.vacancy_schema import VacancySchemaRel, VacancyAddSchema
from backend.core.services.vacancies.repository import VacancyRepository
from backend.core.utils.const import EMPLOYER_USER_TYPE
from backend.core.utils.exc import vacancy_not_found_exc, user_is_not_owner_exc, user_dont_have_company_exc, \
    user_have_this_profession_exc
from backend.core.utils.other.type_utils import UserVar


class VacancyService:

    def __init__(self, vacancy_repo: VacancyRepository):
        self.vacancy_repo = vacancy_repo

    async def create_vacancy(
            self, company_id: int, employer: EmployerSchema, new_vacancy: VacancyAddSchema
    ) -> VacancySchema:
        if not employer.company_id:
            raise user_dont_have_company_exc
        if not employer.is_owner:
            raise user_is_not_owner_exc

        try:
            vacancy = await self.vacancy_repo.create_vacancy(
                company_id=company_id,
                profession_id=new_vacancy.profession_id,
                salary_first=new_vacancy.salary_first,
                salary_second=new_vacancy.salary_second,
                description=new_vacancy.description,
                city=new_vacancy.city
            )
        except IntegrityError:
            raise user_have_this_profession_exc
        schema = VacancySchema.model_validate(vacancy)
        return schema

    async def get_vacancy(self, vacancy_id: int) -> VacancySchema:
        vacancy = await self.vacancy_repo.get_vacancy(id=vacancy_id)
        if not vacancy:
            raise vacancy_not_found_exc
        schema = VacancySchema.model_validate(vacancy)
        return schema

    async def get_vacancy_rel(self, vacancy_id: int) -> VacancySchemaRel:
        vacancy = await self.vacancy_repo.get_vacancy_rel(id=vacancy_id)
        if not vacancy:
            raise vacancy_not_found_exc
        schema = VacancySchemaRel.model_validate(vacancy)
        return schema

    async def update_vacancy(self, vacancy_id: int, employer: EmployerSchema, **kwargs) -> VacancySchema:
        vacancy = await self.vacancy_repo.update_vacancy(vacancy_id=vacancy_id, **kwargs)
        if not vacancy:
            raise vacancy_not_found_exc
        if not (vacancy.company_id == employer.company_id and employer.is_owner):
            raise user_is_not_owner_exc
        schema = VacancySchema.model_validate(vacancy)
        return schema

    async def delete_vacancy(self, vacancy_id: int, employer: EmployerSchema) -> None:
        vacancy = await self.vacancy_repo.delete_vacancy(vacancy_id=vacancy_id)
        if not vacancy:
            raise vacancy_not_found_exc
        if not (vacancy.company_id == employer.company_id and employer.is_owner):
            raise user_is_not_owner_exc

    async def search_vacancy(self, user: UserVar, **kwargs) -> Sequence[VacancySchema]:
        company_id = None
        if user:
            if user.type == EMPLOYER_USER_TYPE:
                company_id = user.company_id
        vacancies = await self.vacancy_repo.search_vacancy(company_id=company_id, **kwargs)
        schemas = [VacancySchemaRel.model_validate(vacancy) for vacancy in vacancies]
        return schemas
