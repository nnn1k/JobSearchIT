from typing import Optional

from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import  selectinload

from backend.core.database.models.employer import VacanciesOrm
from backend.core.database.models.other import ProfessionsOrm
from backend.core.schemas import  VacancySchemaRel
from backend.core.utils.const import EMPLOYER_USER_TYPE
from backend.core.utils.other.type_utils import UserVar


async def get_all_vacancies_query(user: UserVar, session: AsyncSession, **kwargs):
    stmt = (
        select(VacanciesOrm)
        .join(ProfessionsOrm)
        .options(selectinload(VacanciesOrm.company))
        .options(selectinload(VacanciesOrm.profession))
    )

    min_salary: Optional[int] = kwargs.get('min_salary', None)
    profession: Optional[str] = kwargs.get('profession', None)
    city: Optional[str] = kwargs.get('city', None)
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
        conditions.append(ProfessionsOrm.title.ilike(f'%{profession}%'))
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
    schemas = [VacancySchemaRel.model_validate(vacancy, from_attributes=True) for vacancy in vacancies]
    return schemas, kwargs


