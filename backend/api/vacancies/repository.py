from backend.database.models.employer import VacanciesOrm
from backend.api.vacancies.schemas import VacancySchema
from backend.database.utils.repository import AlchemyRepository


class VacancyRepository(AlchemyRepository):
    db_model = VacanciesOrm
    schema = VacancySchema


def get_vacancy_repo():
    return VacancyRepository()


async def get_vacancy_by_id(vacancy_id: int):
    vacancy_repo = get_vacancy_repo()
    vacancy = await vacancy_repo.get_one(id=vacancy_id)
    return vacancy
