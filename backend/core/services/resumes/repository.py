from typing import Sequence, Optional

from sqlalchemy import insert, select, update, delete, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.core.database.models.other import ProfessionsOrm
from backend.core.database.models.worker import ResumesOrm


class ResumeRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_resume(
            self,
            profession_id: int,
            salary_first: int,
            salary_second: int,
            description: str,
            city: str,
            worker_id: int
    ) -> ResumesOrm:
        stmt = (
            insert(ResumesOrm)
            .values(
                profession_id=profession_id,
                salary_first=salary_first,
                salary_second=salary_second,
                description=description,
                city=city,
                worker_id=worker_id
            )
            .returning(ResumesOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_resume(self, **kwargs) -> ResumesOrm:
        stmt = (
            select(ResumesOrm)
            .filter_by(**kwargs)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_resume_rel(self, **kwargs) -> ResumesOrm:
        stmt = (
            select(ResumesOrm)
            .filter_by(**kwargs)
            .options(selectinload(ResumesOrm.worker))
            .options(selectinload(ResumesOrm.skills))
            .options(selectinload(ResumesOrm.profession))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_resumes_rel(self, **kwargs) -> ResumesOrm:
        stmt = (
            select(ResumesOrm)
            .filter_by(**kwargs)
            .options(selectinload(ResumesOrm.worker))
            .options(selectinload(ResumesOrm.skills))
            .options(selectinload(ResumesOrm.profession))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_resume(
            self,
            resume_id: int,
            profession_id: int,
            salary_first: int,
            salary_second: int,
            description: str,
            city: str,
    ) -> ResumesOrm:
        stmt = (
            update(ResumesOrm)
            .filter_by(id=resume_id)
            .values(
                profession_id=profession_id,
                salary_first=salary_first,
                salary_second=salary_second,
                description=description,
                city=city
            )
            .returning(ResumesOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def delete_resume(self, resume_id: int) -> ResumesOrm:
        stmt = (
            delete(ResumesOrm)
            .filter_by(id=resume_id)
            .returning(ResumesOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def search_resume(self, **kwargs) -> Sequence[ResumesOrm]:
        stmt = (
            select(ResumesOrm)
            .join(ProfessionsOrm)
            .options(selectinload(ResumesOrm.profession))
        )
        max_salary: Optional[int] = kwargs.get("max_salary", None)
        profession: Optional[str] = kwargs.get("profession", None)
        city: Optional[str] = kwargs.get("city", None)
        if isinstance(city, str):
            city = city.strip()
        if isinstance(profession, str):
            profession = profession.strip()
        conditions = []
        if city:
            conditions.append(ResumesOrm.city == city)
        if max_salary:
            conditions.append(ResumesOrm.salary_second <= max_salary)
        if profession:
            conditions.append(ProfessionsOrm.title.ilike(f'%{profession}%'))
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = stmt.order_by(desc(ResumesOrm.updated_at))
        result = await self.session.execute(stmt)
        return result.scalars().all()
