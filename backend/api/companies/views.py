from fastapi import Depends, APIRouter, HTTPException, status

from backend.api.companies.queries import create_company_queries, get_company_by_id_queries, update_company_queries
from backend.api.companies.schemas import CompanyAddSchema, CompanyUpdateSchema
from backend.utils.auth_utils.user_login_dependencies import get_employer_by_token, get_user_by_token
from backend.schemas import CompanySchema
from backend.schemas import EmployerResponseSchema
from backend.utils.auth_utils.check_func import check_employer_can_update

router = APIRouter(prefix='/companies', tags=['companies'])


@router.post('/', summary='Создать компанию')
async def create_new_company(
        company: CompanyAddSchema,
        user: EmployerResponseSchema = Depends(get_employer_by_token)
):
    if user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user have company'
        )
    company, user = await create_company_queries(user, **company.model_dump())
    return {
        'status': 'ok',
        'company': company,
        'user': user
    }


@router.get('/{company_id}', summary='Посмотреть информацию о компании')
async def get_info_on_company(
        company_id: int,
        user=Depends(get_user_by_token)
):
    company = await get_company_by_id_queries(company_id)
    can_update = check_employer_can_update(user, company)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='company is not exist'
        )
    return {
        'status': 'ok',
        'company': company,
        'user': user,
        'can_update': can_update
    }


@router.put('/{company_id}', summary='Изменить описание компании')
async def update_company(
        new_company: CompanyUpdateSchema,
        company_id: int,
        user: EmployerResponseSchema = Depends(get_employer_by_token)
):
    company = await update_company_queries(company_id, user, **new_company.model_dump())
    if not company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='error'
        )
    return {
        'status': 'ok',
        'company': company,
        'user': user
    }
