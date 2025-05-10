from typing import Optional

from sqlalchemy import select, update, insert, delete, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from backend.core.database.models.employer import VacanciesOrm
from backend.core.database.models.other import ProfessionsOrm
from backend.core.utils.const import EMPLOYER_USER_TYPE
from backend.core.utils.other.type_utils import UserVar


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
            .options(selectinload(VacanciesOrm.responses))
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

    async def search_vacancy(self, company_id: Optional[int], **kwargs):
        stmt = (
            select(VacanciesOrm)
            .join(ProfessionsOrm)
            .options(selectinload(VacanciesOrm.company))
            .options(selectinload(VacanciesOrm.profession))
            .options(selectinload(VacanciesOrm.responses))
            .order_by(desc(VacanciesOrm.updated_at))
        )

        min_salary: Optional[int] = kwargs.get('min_salary', None)
        profession: Optional[str] = kwargs.get('profession', None)
        city: Optional[str] = kwargs.get('city', None)
        if isinstance(city, str):
            city = city.strip()
        if isinstance(profession, str):
            profession = profession.strip()
        conditions = []
        if city:
            conditions.append(VacanciesOrm.city == city)
        if min_salary:
            conditions.append(VacanciesOrm.salary_first >= min_salary)
        if profession:
            conditions.append(ProfessionsOrm.title.ilike(f'%{profession}%'))
        if company_id:
            conditions.append(VacanciesOrm.company_id != company_id)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        result = await self.session.execute(stmt)
        return result.scalars().all()
