from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.utils.dependencies import get_db
from backend.core.services.vacancies.repository import VacancyRepository
from backend.core.services.vacancies.service import VacancyService


def get_vacancy_repo(session: AsyncSession = Depends(get_db)) -> VacancyRepository:
    return VacancyRepository(session=session)


def get_vacancy_serv(vacancy_repo: VacancyRepository = Depends(get_vacancy_repo)) -> VacancyService:
    return VacancyService(vacancy_repo=vacancy_repo)
