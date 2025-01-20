from fastapi import Depends, APIRouter

from backend.api.companies.dependencies import create_company_dependencies
from backend.api.companies.schemas import CompanySchema
from backend.api.users.employers.schemas import EmployerSchema

router = APIRouter(prefix='/companies')


@router.get('/', summary='Создать компанию')
def create_new_company(
        company: CompanySchema, owner: EmployerSchema = Depends(create_company_dependencies)
):
    return {'company': company, 'owner': owner}
