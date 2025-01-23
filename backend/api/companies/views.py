from fastapi import Depends, APIRouter, Cookie

from backend.api.companies.dependencies import create_company_dependencies, update_company_dependencies
from backend.api.companies.repository import get_company_by_id
from backend.api.companies.schemas import CompanySchema, CompanyAddSchema
from backend.api.users.auth.token_dependencies import get_user_by_token
from backend.api.users.employers.schemas import EmployerSchema
from backend.schemas.global_schema import UserSchema

router = APIRouter(prefix='/companies')


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


@router.get('/<company_id>', summary='Посмотреть информацию о компании')
def get_info_on_company(
        company: CompanySchema = Depends(get_company_by_id),
        user=Depends(get_user_by_token)
):

    return {
        'status': 'ok',
        'company': company,
        'user': user.model_dump(exclude='password')
    }

@router.put('/<company_id>', summary='Изменить описание компании')
def update_company(
        company_and_user: CompanySchema = Depends(update_company_dependencies),

):
    company, user = company_and_user
    return {
        'status': 'ok',
        'company': company,
        'user': user.model_dump(exclude='password')
    }
