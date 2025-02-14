from sqlalchemy import select, update
from sqlalchemy.orm import joinedload, selectinload

from backend.database.models.employer import CompaniesOrm, EmployersOrm
from backend.database.settings.database import session_factory
from backend.schemas.models.employer.employer_schema import EmployerResponseSchema


async def get_employer_by_id_queries(employer_id: int):
    async with session_factory() as session:
        stmt = await session.execute(
            select(EmployersOrm)
            .options(joinedload(EmployersOrm.company).selectinload(CompaniesOrm.vacancies))
            .filter_by(id=int(employer_id))
        )
        employer = stmt.scalars().one_or_none()
        return EmployerResponseSchema.model_validate(employer, from_attributes=True)


async def update_employer_by_id_queries(employer_id: int, **kwargs):
    async with session_factory() as session:
        stmt = await session.execute(
            update(EmployersOrm)
            .filter_by(id=int(employer_id))
            .values(**kwargs)
            .returning(EmployersOrm)
            .options(selectinload(EmployersOrm.company).selectinload(CompaniesOrm.vacancies))
        )
        employer = stmt.scalars().one_or_none()
        schema = EmployerResponseSchema.model_validate(employer, from_attributes=True)
        await session.commit()
        return schema
