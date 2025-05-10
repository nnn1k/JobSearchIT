from sqlalchemy import select, and_, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from backend.core.database.models.employer import EmployersOrm, CompaniesOrm
from backend.core.database.models.worker import WorkersOrm, ResumesOrm


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_worker(self, **kwargs) -> WorkersOrm:
        stmt = (
            select(WorkersOrm)
            .filter_by(**kwargs)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_employer(self, **kwargs) -> EmployersOrm:
        stmt = (
            select(EmployersOrm)
            .filter_by(**kwargs)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_worker_rel(self, **kwargs) -> WorkersOrm:
        stmt = (
            select(WorkersOrm)
            .filter_by(**kwargs)
            .options(
                selectinload(WorkersOrm.resumes).selectinload(ResumesOrm.profession)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_employer_rel(self, **kwargs) -> EmployersOrm:
        stmt = (
            select(EmployersOrm)
            .filter_by(**kwargs)
            .options(joinedload(EmployersOrm.company).selectinload(CompaniesOrm.vacancies))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create_worker(self, email: str, password: bytes) -> WorkersOrm:
        stmt = (
            insert(WorkersOrm)
            .values(email=email, password=password)
            .returning(WorkersOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create_employer(self, email: str, password: bytes) -> EmployersOrm:
        stmt = (
            insert(EmployersOrm)
            .values(email=email, password=password)
            .returning(EmployersOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update_worker(self, id: int, **kwargs):
        stmt = (
            update(WorkersOrm)
            .where(and_(WorkersOrm.id == id))
            .values(**kwargs)
            .returning(WorkersOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update_employer(self, id: int, **kwargs):
        stmt = (
            update(EmployersOrm)
            .where(and_(EmployersOrm.id == id))
            .values(**kwargs)
            .returning(EmployersOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
