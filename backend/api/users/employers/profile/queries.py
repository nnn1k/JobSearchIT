from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from backend.database.models.employer import EmployersOrm

from backend.schemas.models.employer.employer_schema import EmployerResponseSchema

from backend.utils.exc import employer_not_found_exc


async def get_employer_by_id_queries(employer_id: int, session: AsyncSession) -> EmployerResponseSchema:
    stmt = await session.execute(
        select(EmployersOrm)
        .options(joinedload(EmployersOrm.company))
        .filter_by(id=int(employer_id))
    )
    employer = stmt.scalars().one_or_none()
    if not employer:
        raise employer_not_found_exc

    schema = EmployerResponseSchema.model_validate(employer, from_attributes=True)
    return schema


async def update_employer_by_id_queries(employer_id: int, session: AsyncSession, **kwargs):
    stmt = await session.execute(
        update(EmployersOrm)
        .filter_by(id=int(employer_id))
        .values(**kwargs)
        .returning(EmployersOrm)
        .options(selectinload(EmployersOrm.company))
    )
    employer = stmt.scalars().one_or_none()
    if not employer:
        raise employer_not_found_exc

    schema = EmployerResponseSchema.model_validate(employer, from_attributes=True)
    await session.commit()
    return schema
