from typing import Annotated

from fastapi import Depends, HTTPException, status

from backend.api.companies.repository import get_company_repo, get_company_by_id
from backend.api.companies.schemas import CompanyAddSchema, CompanyUpdateSchema, CompanySchema
from backend.api.users.auth.token_dependencies import get_user_by_token
from backend.api.users.employers.dependencies import get_employer_by_token
from backend.api.users.employers.repository import get_employer_repo
from backend.api.users.employers.schemas import EmployerSchema


async def create_company_dependencies(
        company: CompanyAddSchema,
        owner: EmployerSchema = Depends(get_employer_by_token)
):
    company_repo = get_company_repo()
    company = await company_repo.add_one(name=company.name, description=company.description)
    employer_repo = get_employer_repo()
    employer = await employer_repo.update_one(id=owner.id, company_id=company.id, is_owner=True)
    return company, employer


async def update_company_dependencies(
        new_company: CompanyUpdateSchema,
        company: CompanySchema = Depends(get_company_by_id),
        user: Annotated['EmployerSchema', 'WorkerSchema'] = Depends(get_user_by_token)
):
    try:
        if user.is_owner and user.company_id == company.id:
            company_repo = get_company_repo()
            company = await company_repo.update_one(id=company.id, description=new_company.description)
            return company, user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no rights"
        )
