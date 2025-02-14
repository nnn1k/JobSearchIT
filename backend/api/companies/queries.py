from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload

from backend.database.models.employer import CompaniesOrm, EmployersOrm
from backend.database.settings.database import session_factory
from backend.schemas import EmployerResponseSchema
from backend.schemas.models.employer.company_schema import CompanySchema

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


async def get_company_by_id_queries(company_id):
    async with session_factory() as session:
        stmt = await session.execute(
            select(CompaniesOrm)
            .options(selectinload(CompaniesOrm.vacancies))
            .where(CompaniesOrm.id == company_id)
        )
        company = stmt.scalars().one_or_none()
        if not company:
            return None
        return CompanySchema.model_validate(company, from_attributes=True)

async def update_company_queries(company_id, owner: EmployerResponseSchema, **kwargs):
    async with session_factory() as session:
        stmt = await session.execute(
            update(CompaniesOrm)
            .values(**kwargs)
            .filter_by(id=company_id)
            .returning(CompaniesOrm)
            .options(selectinload(CompaniesOrm.vacancies))
        )
        company = stmt.scalars().one_or_none()
        if not company:
            return None
        schema = CompanySchema.model_validate(company, from_attributes=True)
        if owner.company_id == company.id and owner.is_owner:
            await session.commit()
            return schema
        return None