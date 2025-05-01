from typing import Optional

from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from backend.core.database.models.employer import VacanciesOrm


class VacancyRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_vacancy(
            self,
            company_id: int,
            profession_id: int,
            salary_first: Optional[int],
            salary_second: Optional[int],
            description: str,
            city: Optional[str],
    ) -> VacanciesOrm:
        stmt = (
            insert(VacanciesOrm)
            .values(
                company_id=company_id,
                profession_id=profession_id,
                salary_first=salary_first,
                salary_second=salary_second,
                description=description,
                city=city
            )
            .returning(VacanciesOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_vacancy(self, **kwargs) -> VacanciesOrm:
        stmt = (
            select(VacanciesOrm)
            .filter_by(**kwargs)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_vacancy_rel(self, **kwargs) -> VacanciesOrm:
        stmt = (
            select(VacanciesOrm)
            .filter_by(**kwargs)
            .options(joinedload(VacanciesOrm.company))
            .options(selectinload(VacanciesOrm.skills))
            .options(selectinload(VacanciesOrm.profession))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update_vacancy(self, vacancy_id: int, **kwargs) -> VacanciesOrm:
        stmt = (
            update(VacanciesOrm)
            .filter_by(id=vacancy_id)
            .values(**kwargs)
            .returning(VacanciesOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def delete_vacancy(self, vacancy_id: int) -> VacanciesOrm:
        stmt = (
            delete(VacanciesOrm)
            .filter_by(id=vacancy_id)
            .returning(VacanciesOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()