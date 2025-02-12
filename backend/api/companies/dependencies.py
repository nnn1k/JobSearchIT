from typing import Tuple, Optional

from fastapi import Depends, HTTPException, status

from backend.api.companies.queries import (
    create_company_queries,
    get_company_by_id_queries,
    update_company_queries
)
from backend.api.companies.schemas import CompanyAddSchema, CompanyUpdateSchema
from backend.schemas import CompanySchema
from backend.utils.auth_utils.token_dependencies import get_user_by_token
from backend.api.users.employers.profile.dependencies import get_employer_by_token
from backend.schemas import EmployerResponseSchema
from backend.schemas import VacancySchema
from backend.utils.auth_utils.check_func import check_employer_can_update
from backend.utils.other.type_utils import UserVar


async def get_company_by_id_dependencies(
        company_id: int,
        user=Depends(get_user_by_token)
) -> Tuple[CompanySchema, UserVar, bool, VacancySchema | None]:
    company = await get_company_by_id_queries(company_id)
    can_update = check_employer_can_update(user, company)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='company is not exist'
        )
    return company, user, can_update


async def create_company_dependencies(
        company: CompanyAddSchema,
        owner: EmployerResponseSchema = Depends(get_employer_by_token)
) -> Tuple[Optional[CompanySchema], UserVar]:
    if owner.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user have company'
        )
    company, owner = await create_company_queries(owner, **company.model_dump())
    return company, owner


async def update_company_dependencies(
        new_company: CompanyUpdateSchema,
        company_id: int,
        owner: EmployerResponseSchema = Depends(get_employer_by_token)

) -> tuple[CompanySchema | None, EmployerResponseSchema]:
    company = await update_company_queries(company_id, owner, **new_company.model_dump())
    if not company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='error'
        )
    return company, owner
