from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload

from backend.database.models.employer import CompaniesOrm, EmployersOrm
from backend.database.settings.database import session_factory
from backend.schemas import EmployerResponseSchema
from backend.schemas.models.employer.company_schema import CompanySchema
from backend.utils.other.celery_utils import cl_app
from backend.modules.redis.redis_utils import cache_object, get_cached_object
from backend.utils.str_const import COMPANY_TYPE


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
        await cache_object(company_schema)
        await cache_object(employer_schema)
        return company_schema, employer_schema


@cl_app.task
async def get_company_by_id_queries(company_id: int, refresh: bool = False):
    if not refresh:
        cache_company = await get_cached_object(obj_type=COMPANY_TYPE, obj_id=company_id, schema=CompanySchema)
        if cache_company:
            return cache_company
    async with session_factory() as session:
        stmt = await session.execute(
            select(CompaniesOrm)
            .options(selectinload(CompaniesOrm.vacancies))
            .where(CompaniesOrm.id == company_id)
        )
        company = stmt.scalars().one_or_none()
        if not company:
            return None
        schema = CompanySchema.model_validate(company, from_attributes=True)
        await cache_object(schema)
        return schema


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
            await cache_object(schema)
            return schema
        return None
