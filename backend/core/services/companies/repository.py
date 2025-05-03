from typing import Sequence

from sqlalchemy import select, update, and_, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from backend.core.database.models.employer import CompaniesOrm, VacanciesOrm
from backend.core.database.models.other.Review import ReviewsOrm


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
            .options(selectinload(CompaniesOrm.reviews))
            .options(selectinload(CompaniesOrm.vacancies).selectinload(VacanciesOrm.responses))
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

    async def delete_company(self, id: int) -> CompaniesOrm:
        stmt = (
            delete(CompaniesOrm)
            .filter_by(id=id)
            .returning(CompaniesOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def add_review(self, worker_id: int, company_id: int, score: int, message: str) -> ReviewsOrm:
        stmt = (
            insert(ReviewsOrm)
            .values(worker_id=worker_id, company_id=company_id, score=score, message=message)
            .returning(ReviewsOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update_review(self, review_id: int, score: int, message: str) -> ReviewsOrm:
        stmt = (
            update(ReviewsOrm)
            .where(and_(ReviewsOrm.id == review_id))
            .values(score=score, message=message)
            .returning(ReviewsOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_reviews(self, **kwargs) -> Sequence[ReviewsOrm]:
        stmt = (
            select(ReviewsOrm)
            .filter_by(**kwargs)
            .options(joinedload(ReviewsOrm.worker))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_review(self, **kwargs) -> ReviewsOrm:
        stmt = (
            select(ReviewsOrm)
            .filter_by(**kwargs)
            .options(joinedload(ReviewsOrm.worker))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def delete_review(self, review_id: int) -> ReviewsOrm:
        stmt = (
            delete(ReviewsOrm)
            .filter_by(id=review_id)
            .returning(ReviewsOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()


