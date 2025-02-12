from fastapi import Depends, APIRouter

from backend.api.companies.dependencies import (
    create_company_dependencies,
    update_company_dependencies,
    get_company_by_id_dependencies
)
from backend.schemas import CompanySchema
from backend.schemas import EmployerResponseSchema

router = APIRouter(prefix='/companies', tags=['companies'])


@router.post('/', summary='Создать компанию')
def create_new_company(
        company_and_user: EmployerResponseSchema = Depends(create_company_dependencies)
):
    company, user = company_and_user
    return {
        'status': 'ok',
        'company': company,
        'user': user
    }


@router.get('/{company_id}', summary='Посмотреть информацию о компании')
def get_info_on_company(
        company_and_user: CompanySchema = Depends(get_company_by_id_dependencies),
):
    company, user, can_update = company_and_user
    return {
        'status': 'ok',
        'company': company,
        'user': user,
        'can_update': can_update
    }


@router.put('/{company_id}', summary='Изменить описание компании')
def update_company(
        company_and_user: CompanySchema = Depends(update_company_dependencies),

):
    company, user = company_and_user
    return {
        'status': 'ok',
        'company': company,
        'user': user
    }
