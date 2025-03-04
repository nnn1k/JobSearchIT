from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.companies.queries import create_company_queries, delete_company_queries, get_company_by_id_queries, \
    update_company_queries
from backend.api.companies.schemas import CompanyAddSchema, CompanyUpdateSchema
from backend.database.utils.dependencies import get_db
from backend.utils.auth_utils.user_login_dependencies import get_employer_by_token, get_user_by_token
from backend.schemas import EmployerResponseSchema
from backend.utils.auth_utils.check_func import check_employer_can_update
from backend.utils.other.time_utils import time_it_async

router = APIRouter(prefix='/companies', tags=['companies'])


@router.post('', summary='Создать компанию')
@time_it_async
async def create_new_company(
        company: CompanyAddSchema,
        user: EmployerResponseSchema = Depends(get_employer_by_token),
        session: AsyncSession = Depends(get_db),
):
    company, user = await create_company_queries(employer=user, session=session, **company.model_dump())
    return {
        'status': 'ok',
        'company': company,
    }


@router.get('/{company_id}', summary='Посмотреть информацию о компании')
@time_it_async
async def get_info_on_company(
        company_id: int,
        user=Depends(get_user_by_token),
        session: AsyncSession = Depends(get_db),
):
    company = await get_company_by_id_queries(company_id, session=session)
    can_update = check_employer_can_update(user, company)
    return {
        'status': 'ok',
        'company': company,
        'can_update': can_update
    }


@router.put('/{company_id}', summary='Изменить описание компании')
@time_it_async
async def update_company(
        new_company: CompanyUpdateSchema,
        company_id: int,
        user: EmployerResponseSchema = Depends(get_employer_by_token),
        session: AsyncSession = Depends(get_db),
):
    company = await update_company_queries(company_id=company_id, owner=user, session=session, **new_company.model_dump())
    return {
        'status': 'ok',
        'company': company,
    }

@router.delete('/{company_id}', summary='Удалить компанию')
@time_it_async
async def delete_company(
        company_id: int,
        user: EmployerResponseSchema = Depends(get_employer_by_token),
        session: AsyncSession = Depends(get_db),
):
    await delete_company_queries(company_id=company_id, owner=user, session=session)
    return {
        'status': 'ok'
    }
