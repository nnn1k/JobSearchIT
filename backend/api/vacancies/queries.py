from sqlalchemy import insert, select, update
from sqlalchemy.orm import joinedload, selectinload

from backend.database.models.employer import VacanciesOrm
from backend.database.settings.database import session_factory
from backend.schemas import EmployerResponseSchema, VacancySchema

from backend.utils.other.celery_utils import cl_app


async def create_vacancy_queries(company_id, **kwargs):
    async with session_factory() as session:
        stmt = await session.execute(
            insert(VacanciesOrm)
            .values(company_id=company_id, **kwargs)
            .returning(VacanciesOrm)
            .options(selectinload(VacanciesOrm.company))
            .options(selectinload(VacanciesOrm.skills))
        )
        vacancy = stmt.scalars().one_or_none()
        if not vacancy:
            return None
        schema = VacancySchema.model_validate(vacancy, from_attributes=True)
        await session.commit()
        return schema


@cl_app.task
async def get_vacancy_by_id_queries(vacancy_id: int, refresh: bool = False):
    if not refresh:
        ...
    async with session_factory() as session:
        stmt = await session.execute(
            select(VacanciesOrm)
            .options(joinedload(VacanciesOrm.company))
            .options(selectinload(VacanciesOrm.skills))
            .filter_by(id=vacancy_id, deleted_at=None)
        )
        vacancy = stmt.scalars().one_or_none()
        if not vacancy:
            return None
        schema = VacancySchema.model_validate(vacancy, from_attributes=True)
        return schema


async def update_vacancy_by_id_queries(vacancy_id, owner: EmployerResponseSchema, **kwargs):
    if not owner.is_owner:
        return None
    async with session_factory() as session:
        stmt = await session.execute(
            update(VacanciesOrm)
            .values(**kwargs)
            .filter_by(id=vacancy_id)
            .returning(VacanciesOrm)
        )
        vacancy = stmt.scalars().one_or_none()
        if not vacancy:
            return None
        if owner.company_id == vacancy.company_id:
            await session.commit()
            return await get_vacancy_by_id_queries(vacancy_id)
        return None
