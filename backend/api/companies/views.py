from fastapi import Depends, APIRouter

from backend.api.companies.dependencies import create_company_dependencies
from backend.api.companies.schemas import CompanySchema
from backend.api.users.employers.schemas import EmployerSchema

router = APIRouter(prefix='/companies')


@router.post('/', summary='Создать компанию')
def create_new_company(
        company: CompanySchema, owner: EmployerSchema = Depends(create_company_dependencies)
):
    return {'company': company, 'owner': owner}

@router.get('/', summary='Посмотреть информацию о своей компании')
def get_info_on_company(

):
    pass
