from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from backend.database.models.employer import CompaniesOrm, EmployersOrm
from backend.database.settings.database import session_factory
from backend.schemas import EmployerResponseSchema
from backend.schemas.models.employer.company_schema import CompanySchema
from backend.database.models.employer import VacanciesOrm

from fastapi import HTTPException, status

from backend.utils.exc import company_not_found_exc, employer_not_found_exc, user_have_company_exc, \
    user_is_not_owner_exc


async def create_company_queries(employer: EmployerResponseSchema, session: AsyncSession, **kwargs):
    if employer.company_id:
        raise user_have_company_exc

    stmt = await session.execute(
        insert(CompaniesOrm)
        .values(**kwargs)
        .returning(CompaniesOrm)
    )
    company = stmt.scalars().one_or_none()
    if not company:
        raise company_not_found_exc

    stmt = await session.execute(
        update(EmployersOrm)
        .values(company_id=company.id, is_owner=True)
        .filter_by(id=employer.id)
        .returning(EmployersOrm)
    )
    employer = stmt.scalars().one_or_none()
    if not employer:
        raise employer_not_found_exc

    company_schema = CompanySchema.model_validate(company, from_attributes=True)
    employer_schema = EmployerResponseSchema.model_validate(employer, from_attributes=True)
    await session.commit()
    return company_schema, employer_schema


async def get_company_by_id_queries(company_id: int, session: AsyncSession):
    stmt = await session.execute(
        select(CompaniesOrm)
        .outerjoin(CompaniesOrm.vacancies)
        .filter(CompaniesOrm.id == company_id)
        .options(
            contains_eager(CompaniesOrm.vacancies)
            .selectinload(VacanciesOrm.profession)
        )
    )
    company = stmt.scalars().unique().one_or_none()
    if not company:
        raise company_not_found_exc
    schema = CompanySchema.model_validate(company, from_attributes=True)
    return schema


async def update_company_queries(company_id, owner: EmployerResponseSchema, session: AsyncSession, **kwargs):
    if not (owner.company_id == company_id and owner.is_owner):
        raise user_is_not_owner_exc

    stmt = await session.execute(
        update(CompaniesOrm)
        .values(**kwargs)
        .filter_by(id=company_id)
        .returning(CompaniesOrm)
    )
    company = stmt.scalars().one_or_none()
    if not company:
        raise company_not_found_exc
    await session.commit()
    return await get_company_by_id_queries(company_id, session)


async def delete_company_queries(company_id: int, owner: EmployerResponseSchema, session: AsyncSession):
    if not (company_id == owner.company_id and owner.is_owner):
        raise user_is_not_owner_exc

    stmt = await session.execute(
        delete(CompaniesOrm)
        .filter_by(id=company_id)
        .returning(CompaniesOrm)
    )
    company = stmt.scalars().one_or_none()
    if not company:
        raise company_not_found_exc
    stmt = await session.execute(
        update(EmployersOrm)
        .values(company_id=None, is_owner=False)
        .filter_by(id=owner.id)
    )
    employer = stmt.scalars().one_or_none()
    if not employer:
        raise employer_not_found_exc
    await session.commit()
