
from sqlalchemy import insert, select, update, or_
from sqlalchemy.orm import contains_eager

from backend.database.models.employer import CompaniesOrm, EmployersOrm
from backend.database.settings.database import session_factory
from backend.schemas import EmployerResponseSchema
from backend.schemas.models.employer.company_schema import CompanySchema
from backend.database.models.employer import VacanciesOrm

from fastapi import HTTPException, status

async def create_company_queries(employer: EmployerResponseSchema, **kwargs):
    async with session_factory() as session:
        stmt = await session.execute(
            insert(CompaniesOrm)
            .values(**kwargs)
            .returning(CompaniesOrm)
        )
        company = stmt.scalars().one_or_none()
        if not company:
            return None

        stmt = await session.execute(
            update(EmployersOrm)
            .values(company_id=company.id, is_owner=True)
            .filter_by(id=employer.id)
            .returning(EmployersOrm)
        )
        employer = stmt.scalars().one_or_none()
        if not employer:
            return None

        company_schema = CompanySchema.model_validate(company, from_attributes=True)
        employer_schema = EmployerResponseSchema.model_validate(employer, from_attributes=True)
        await session.commit()
        return company_schema, employer_schema


async def get_company_by_id_queries(company_id: int, refresh: bool = False):
    if not refresh:
        ...
    async with session_factory() as session:
        stmt = await session.execute(
            select(CompaniesOrm)
            .outerjoin(CompaniesOrm.vacancies)
            .filter(CompaniesOrm.id == company_id)
            .options(
                contains_eager(CompaniesOrm.vacancies).selectinload(VacanciesOrm.profession)
            )
        )
        company = stmt.scalars().unique().one_or_none()
        company.vacancies = [vacancy for vacancy in company.vacancies if vacancy.deleted_at is None]
        if not company:
            return None
        schema = CompanySchema.model_validate(company, from_attributes=True)
        return schema


async def update_company_queries(company_id, owner: EmployerResponseSchema, **kwargs):
    if not (owner.company_id == company_id and owner.is_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user is not owner in company'
        )
    async with session_factory() as session:
        stmt = await session.execute(
            update(CompaniesOrm)
            .values(**kwargs)
            .filter_by(id=company_id, deleted_at=None)
            .returning(CompaniesOrm)
        )
        company = stmt.scalars().one_or_none()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='company is not exist'
            )
        await session.commit()
    return await get_company_by_id_queries(company_id, refresh=True)

async def delete_company_queries(company_id: int, owner: EmployerResponseSchema):
    if not (company_id == owner.company_id and owner.is_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user is not owner in company'
        )
    async with session_factory() as session:
        from sqlalchemy import delete
        stmt = await session.execute(
            delete(CompaniesOrm)
            .filter_by(id=company_id)
            .returning(CompaniesOrm)
        )
        company = stmt.scalars().one_or_none()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='company not found'
            )
        stmt = await session.execute(
            update(EmployersOrm)
            .values(company_id=None, is_owner=False)
            .filter_by(id=owner.id)
        )
        employer = stmt.scalars().one_or_none()
        if not employer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='employer not found'
            )
        await session.commit()
