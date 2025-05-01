from sqlalchemy import select, and_, insert
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.models.employer import EmployersOrm
from backend.core.database.models.worker import WorkersOrm


class AuthRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_worker_by_email(self, email: str) -> WorkersOrm:
        stmt = (
            select(WorkersOrm)
            .where(and_(WorkersOrm.email == email))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_employer_by_email(self, email: str) -> EmployersOrm:
        stmt = (
            select(EmployersOrm)
            .where(and_(EmployersOrm.email == email))
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


