from typing import Optional, List

from backend.database.models.employer.Vacancy import VacanciesOrm
from backend.api.vacancies.schemas import VacancySchema
from backend.database.utils.repository import AlchemyRepository


class VacancyRepository(AlchemyRepository):
    db_model = VacanciesOrm
    schema = VacancySchema


def get_vacancy_repo() -> VacancyRepository:
    return VacancyRepository()


async def get_vacancy_by_id(vacancy_id: int) -> Optional[VacancySchema]:
    vacancy_repo = get_vacancy_repo()
    vacancy = await vacancy_repo.get_one(id=vacancy_id)
    return vacancy


async def get_vacancy_by_company_id(company_id: int) -> Optional[List[VacancySchema]]:
    vacancy_repo = get_vacancy_repo()
    vacancies = await vacancy_repo.get_all(company_id=company_id)
    return vacancies
