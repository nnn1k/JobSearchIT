from backend.database.utils.repository import AlchemyRepository
from backend.database.models.employer import CompaniesOrm
from backend.api.companies.schemas import CompanySchema


class CompanyRepository(AlchemyRepository):
    db_model = CompaniesOrm
    schema = CompanySchema
    user_type = 'company'

def get_company_repo():
    return CompanyRepository()


async def get_company_by_id(company_id: int):
    company_repo = get_company_repo()
    company = await company_repo.get_one(id=company_id)
    return company
