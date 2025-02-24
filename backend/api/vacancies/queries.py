from fastapi import HTTPException, status
from sqlalchemy import and_, desc, insert, select, update, delete
from sqlalchemy.orm import joinedload, selectinload

from backend.database.models.employer import VacanciesOrm
from backend.database.models.other import ProfessionsOrm
from backend.database.models.worker import ResumesOrm, WorkersOrm
from backend.database.settings.database import session_factory
from backend.schemas import EmployerResponseSchema, VacancySchema
from backend.utils.const import WORKER_USER_TYPE
from backend.utils.exc import vacancy_not_found_exc, user_is_not_owner_exc
from backend.utils.other.type_utils import UserVar


async def get_all_vacancies_query(user: UserVar, **kwargs):
    min_salary = kwargs.get('min_salary', None)
    profession = kwargs.get('profession', None)
    city = kwargs.get('city', None)
    start_page = kwargs.get('start_page', None)
    async with session_factory() as session:
        stmt = (
            select(VacanciesOrm)
            .join(ProfessionsOrm)
            .options(selectinload(VacanciesOrm.profession))
        )
        conditions = []
        if city:
            conditions.append(VacanciesOrm.city == city)
        if min_salary:
            conditions.append(VacanciesOrm.salary_first >= min_salary)
        if profession:
            conditions.append(ProfessionsOrm.title.like(f'{profession}%'))
        if start_page and user.type == WORKER_USER_TYPE:
            last_resume = await session.execute(
                select(ResumesOrm)
                .where(and_(ResumesOrm.worker_id == user.id))
                .options(selectinload(ResumesOrm.profession))
                .order_by(desc(ResumesOrm.updated_at))
                .limit(1)
            )
            last_resume = last_resume.scalars().one_or_none()
            conditions.append(ProfessionsOrm.title.like(f'{last_resume.profession.title}%'))
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = stmt.order_by(desc(VacanciesOrm.updated_at))
        result = await session.execute(stmt)
        vacancies = result.scalars().unique().all()
        if not vacancies:
            return []
        schemas = [VacancySchema.model_validate(vacancy, from_attributes=True) for vacancy in vacancies]
        return schemas


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
