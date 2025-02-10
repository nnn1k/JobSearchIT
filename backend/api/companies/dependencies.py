from typing import Tuple, Optional

from fastapi import Depends, HTTPException, status

from backend.api.companies.repository import get_company_repo, get_company_by_id
from backend.api.companies.schemas import CompanyAddSchema, CompanyUpdateSchema, CompanySchema
from backend.utils.auth_utils.token_dependencies import get_user_by_token
from backend.api.users.employers.profile.dependencies import get_employer_by_token
from backend.api.users.employers.profile.repository import get_employer_repo
from backend.api.users.employers.profile.schemas import EmployerResponseSchema
from backend.api.vacancies.repository import get_vacancy_by_company_id
from backend.api.vacancies.schemas import VacancySchema
from backend.utils.auth_utils.check_func import check_employer_can_update
from backend.utils.other.type_utils import UserVar


async def get_company_by_id_dependencies(
        company_id: int,
        user=Depends(get_user_by_token)
) -> Tuple[CompanySchema, UserVar, bool, VacancySchema | None]:
    company = await get_company_by_id(company_id)
    can_update = check_employer_can_update(user, company)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='company is not exist'
        )
    vacancies = await get_vacancy_by_company_id(company_id)
    return company, user, can_update, vacancies


async def create_company_dependencies(
        company: CompanyAddSchema,
        owner: EmployerResponseSchema = Depends(get_employer_by_token)
) -> Tuple[Optional[CompanySchema], UserVar]:
    if owner.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user have company'
        )
    company_repo = get_company_repo()
    company = await company_repo.add_one(**company.model_dump())
    employer_repo = get_employer_repo()
    employer = await employer_repo.update_one(id=owner.id, company_id=company.id, is_owner=True)
    return company, employer


async def update_company_dependencies(
        new_company: CompanyUpdateSchema,
        company_id: int,
        user: EmployerResponseSchema = Depends(get_employer_by_token)

) -> tuple[CompanySchema | None, EmployerResponseSchema]:

    company_repo = get_company_repo()
    company = await company_repo.get_one(id=company_id)
    can_update = check_employer_can_update(user, company)
    if not can_update:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no rights"
            )
    new_company = await company_repo.update_one(id=company_id, **new_company.model_dump())
    return new_company, user
