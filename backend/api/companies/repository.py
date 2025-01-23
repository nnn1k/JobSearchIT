from fastapi import Depends

from backend.api.users.auth.token_dependencies import get_user_by_token
from backend.database.utils.repository import AlchemyRepository
from backend.database.models.employer import CompaniesOrm
from backend.api.companies.schemas import CompanySchema


class CompanyRepository(AlchemyRepository):
    db_model = CompaniesOrm
    schema = CompanySchema
    user_type = 'company'

def get_company_repo():
    return CompanyRepository()


