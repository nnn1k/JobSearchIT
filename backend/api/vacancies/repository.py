from backend.database.models.employer import VacanciesOrm
from backend.api.vacancies.schemas import VacancySchema
from backend.database.utils.repository import AlchemyRepository


class VacancyRepository(AlchemyRepository):
    db_model = VacanciesOrm
    schema = VacancySchema

def get_vacancy_repo():
    return VacancyRepository()