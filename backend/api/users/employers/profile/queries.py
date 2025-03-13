from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.core.database.models.employer import CompaniesOrm, EmployersOrm

from backend.core.schemas.models.employer.employer_schema import EmployerResponseSchema

from backend.core.utils.exc import employer_not_found_exc


async def get_employer_by_id_queries(employer_id: int, session: AsyncSession) -> EmployerResponseSchema:
    result = await session.execute(
        select(EmployersOrm)
        .options(joinedload(EmployersOrm.company).selectinload(CompaniesOrm.vacancies))
        .filter_by(id=int(employer_id))
    )
    employer = result.scalars().one_or_none()
    if not employer:
        raise employer_not_found_exc

    schema = EmployerResponseSchema.model_validate(employer, from_attributes=True)
    return schema


async def update_employer_by_id_queries(employer_id: int, session: AsyncSession, **kwargs):
    result = await session.execute(
        update(EmployersOrm)
        .filter_by(id=int(employer_id))
        .values(**kwargs)
        .returning(EmployersOrm)
        .options(joinedload(EmployersOrm.company).selectinload(CompaniesOrm.vacancies))
    )
    employer = result.scalars().one_or_none()
    if not employer:
        raise employer_not_found_exc

    schema = EmployerResponseSchema.model_validate(employer, from_attributes=True)
    await session.commit()
    return schema
