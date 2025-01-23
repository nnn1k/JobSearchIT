from typing import Annotated

from fastapi import Depends, HTTPException, status

from backend.api.companies.repository import get_company_repo
from backend.api.companies.schemas import CompanyAddSchema, CompanyUpdateSchema, CompanySchema
from backend.api.users.auth.token_dependencies import get_user_by_token
from backend.api.users.employers.dependencies import get_employer_by_token
from backend.api.users.employers.repository import get_employer_repo
from backend.api.users.employers.schemas import EmployerSchema


async def get_company_by_id(
        company_id: int,
        user=Depends(get_user_by_token)
):
    can_update = True
    company_repo = get_company_repo()
    company = await company_repo.get_one(id=company_id)
    if not (hasattr(user, 'company_id') and hasattr(user, 'is_owner')):
        can_update = False
    elif user.company_id != company.id:
        can_update = False
    return company, user, can_update


async def create_company_dependencies(
        company: CompanyAddSchema,
        owner: EmployerSchema = Depends(get_employer_by_token)
):
    if owner.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user have company'
        )
    company_repo = get_company_repo()
    company = await company_repo.add_one(name=company.name, description=company.description)
    employer_repo = get_employer_repo()
    employer = await employer_repo.update_one(id=owner.id, company_id=company.id, is_owner=True)
    return company, employer


async def update_company_dependencies(
        new_company: CompanyUpdateSchema,
        company_and_user: CompanySchema = Depends(get_company_by_id),

):
    company, user, can_update = company_and_user
    try:
        if user.is_owner and user.company_id == company.id:
            company_repo = get_company_repo()
            company = await company_repo.update_one(id=company.id, description=new_company.description)
            return company, user
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no rights"
        )

