from sqlalchemy import select, update
from sqlalchemy.orm import joinedload, selectinload

from backend.database.models.employer import EmployersOrm
from backend.database.settings.database import session_factory
from backend.schemas.models.employer.employer_schema import EmployerResponseSchema

from backend.utils.str_const import EMPLOYER_USER_TYPE

from backend.utils.other.celery_utils import cl_app


@cl_app.task
async def get_employer_by_id_queries(employer_id: int, refresh: bool = False) -> EmployerResponseSchema:
    if not refresh:
       ...
    async with session_factory() as session:
        stmt = await session.execute(
            select(EmployersOrm)
            .options(joinedload(EmployersOrm.company))
            .filter_by(id=int(employer_id), deleted_at=None)
        )
        employer = stmt.scalars().one_or_none()
        schema = EmployerResponseSchema.model_validate(employer, from_attributes=True)
        return schema


async def update_employer_by_id_queries(employer_id: int, **kwargs):
    async with session_factory() as session:
        stmt = await session.execute(
            update(EmployersOrm)
            .filter_by(id=int(employer_id))
            .values(**kwargs)
            .returning(EmployersOrm)
            .options(selectinload(EmployersOrm.company))
        )
        employer = stmt.scalars().one_or_none()
        schema = EmployerResponseSchema.model_validate(employer, from_attributes=True)
        await session.commit()
        return schema
