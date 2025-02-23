from fastapi import HTTPException, status
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import joinedload, selectinload

from backend.database.models.employer import VacanciesOrm
from backend.database.settings.database import session_factory
from backend.schemas import EmployerResponseSchema, VacancySchema
from backend.utils.exc import vacancy_not_found_exc, user_is_not_owner_exc


async def create_vacancy_queries(company_id, user, **kwargs):
    if not user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user dont have company'
        )
    async with session_factory() as session:
        stmt = await session.execute(
            insert(VacanciesOrm)
            .values(company_id=company_id, **kwargs)
            .returning(VacanciesOrm)
            .options(selectinload(VacanciesOrm.company))
            .options(selectinload(VacanciesOrm.skills))
            .options(selectinload(VacanciesOrm.profession))
        )
        vacancy = stmt.scalars().one_or_none()
        if not vacancy:
            return None
        schema = VacancySchema.model_validate(vacancy, from_attributes=True)
        await session.commit()
        return schema


async def get_vacancy_by_id_queries(vacancy_id: int):
    async with session_factory() as session:
        stmt = await session.execute(
            select(VacanciesOrm)
            .options(joinedload(VacanciesOrm.company))
            .options(selectinload(VacanciesOrm.skills))
            .options(selectinload(VacanciesOrm.profession))
            .filter_by(id=vacancy_id)
        )
        vacancy = stmt.scalars().one_or_none()
        if not vacancy:
            raise vacancy_not_found_exc
        schema = VacancySchema.model_validate(vacancy, from_attributes=True)
        return schema


async def update_vacancy_by_id_queries(vacancy_id, owner: EmployerResponseSchema, **kwargs):
    async with session_factory() as session:
        stmt = await session.execute(
            update(VacanciesOrm)
            .values(**kwargs)
            .filter_by(id=vacancy_id)
            .returning(VacanciesOrm)
        )
        vacancy = stmt.scalars().one_or_none()
        if not vacancy:
            raise vacancy_not_found_exc

        if not (owner.company_id == vacancy.company_id and owner.is_owner):
            raise user_is_not_owner_exc
        await session.commit()
        return await get_vacancy_by_id_queries(vacancy_id)


async def delete_vacancy_by_id_queries(vacancy_id: int, owner: EmployerResponseSchema):
    async with session_factory() as session:
        stmt = await session.execute(
            delete(VacanciesOrm)
            .filter_by(id=vacancy_id)
            .returning(VacanciesOrm)
        )
        vacancy = stmt.scalars().one_or_none()
        if not vacancy:
            raise vacancy_not_found_exc
        if not (owner.company_id == vacancy.company_id and owner.is_owner):
            raise user_is_not_owner_exc
        await session.commit()
