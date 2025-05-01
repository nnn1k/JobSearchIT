from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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
    ):
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

    async def get_resume(self, **kwargs):
        stmt = (
            select(ResumesOrm)
            .filter_by(**kwargs)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_resume_rel(self, **kwargs):
        stmt = (
            select(ResumesOrm)
            .filter_by(**kwargs)
            .options(selectinload(ResumesOrm.worker))
            .options(selectinload(ResumesOrm.skills))
            .options(selectinload(ResumesOrm.profession))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update_resume(
            self,
            resume_id: int,
            profession_id: int,
            salary_first: int,
            salary_second: int,
            description: str,
            city: str,
    ):
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

    async def delete_resume(self, resume_id: int):
        stmt = (
            delete(ResumesOrm)
            .filter_by(id=resume_id)
            .returning(ResumesOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
