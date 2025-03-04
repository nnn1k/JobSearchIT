from fastapi import HTTPException, status
from sqlalchemy import and_, desc, insert, or_, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from backend.database.models.employer import VacanciesOrm
from backend.database.models.other import ProfessionsOrm
from backend.database.settings.database import session_factory
from backend.schemas import EmployerResponseSchema, VacancySchema
from backend.utils.const import EMPLOYER_USER_TYPE
from backend.utils.exc import vacancy_not_found_exc, user_is_not_owner_exc
from backend.utils.other.time_utils import time_it_async
from backend.utils.other.type_utils import UserVar


@time_it_async
async def get_all_vacancies_query(user: UserVar, session: AsyncSession, **kwargs):
    stmt = (
        select(VacanciesOrm)
        .join(ProfessionsOrm)
        .options(selectinload(VacanciesOrm.company))
        .options(selectinload(VacanciesOrm.profession))
    )

    min_salary: int = kwargs.get('min_salary', None)
    profession: str = kwargs.get('profession', None)
    city: str = kwargs.get('city', None)
    if isinstance(city, str):
        city = city.strip()
    if isinstance(profession, str):
        profession = profession.strip()
    conditions = []
    if city:
        conditions.append(VacanciesOrm.city == city)
    if min_salary:
        conditions.append(VacanciesOrm.salary_first >= min_salary)
    if profession:
        conditions.append(ProfessionsOrm.title.ilike(f'{profession}%'))
    if user:
        if user.type == EMPLOYER_USER_TYPE:
            conditions.append(VacanciesOrm.company_id != user.company_id)
    if conditions:
        stmt = stmt.where(and_(*conditions))
    stmt = stmt.order_by(desc(VacanciesOrm.updated_at))
    result = await session.execute(stmt)
    vacancies = result.scalars().all()
    if not vacancies:
        return list(), kwargs
    schemas = [VacancySchema.model_validate(vacancy, from_attributes=True) for vacancy in vacancies]
    return schemas, kwargs


async def create_vacancy_queries(company_id, user, session: AsyncSession, **kwargs):
    if not user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user dont have company'
        )

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


async def get_vacancy_by_id_queries(vacancy_id: int, session: AsyncSession):
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


async def update_vacancy_by_id_queries(vacancy_id, owner: EmployerResponseSchema, session: AsyncSession, **kwargs):
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
    return await get_vacancy_by_id_queries(vacancy_id, session)


async def delete_vacancy_by_id_queries(vacancy_id: int, owner: EmployerResponseSchema, session: AsyncSession):
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
