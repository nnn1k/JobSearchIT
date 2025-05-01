from sqlalchemy import select, update, and_, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.core.database.models.employer import CompaniesOrm, VacanciesOrm


class CompanyRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_company(self, name: str, description: str) -> CompaniesOrm:
        stmt = (
            insert(CompaniesOrm)
            .values(name=name, description=description)
            .returning(CompaniesOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_company(self, **kwargs) -> CompaniesOrm:
        stmt = (
            select(CompaniesOrm)
            .filter_by(**kwargs)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_company_rel(self, **kwargs) -> CompaniesOrm:
        stmt = (
            select(CompaniesOrm)
            .filter_by(**kwargs)
            .options(
                selectinload(CompaniesOrm.vacancies).selectinload(VacanciesOrm.profession)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update_company(self, id: int, **kwargs) -> CompaniesOrm:
        stmt = (
            update(CompaniesOrm)
            .where(and_(CompaniesOrm.id == id))
            .values(**kwargs)
            .returning(CompaniesOrm)
        )

        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def delete_company(self, id: int):
        stmt = (
            delete(CompaniesOrm)
            .filter_by(id=id)
            .returning(CompaniesOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
