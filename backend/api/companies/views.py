from fastapi import Depends, APIRouter

from backend.api.companies.dependencies import create_company_dependencies, update_company_dependencies, get_company_by_id
from backend.api.companies.schemas import CompanySchema
from backend.api.users.employers.schemas import EmployerSchema


router = APIRouter(prefix='/companies', tags=['companies'])


@router.post('/', summary='Создать компанию')
def create_new_company(
    owner_and_company: EmployerSchema = Depends(create_company_dependencies)
):
    company, owner = owner_and_company
    return {
        'status': 'ok',
        'company': company,
        'owner': owner
    }


@router.get('/{company_id}', summary='Посмотреть информацию о компании')
def get_info_on_company(
        company_and_user: CompanySchema = Depends(get_company_by_id),
):
    company, user, can_update = company_and_user
    if user:
        user = user.model_dump(exclude='password')
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
    if user:
        user = user.model_dump(exclude='password')
    return {
        'status': 'ok',
        'company': company,
        'user': user
    }
