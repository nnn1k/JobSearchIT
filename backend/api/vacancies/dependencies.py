from typing import Tuple, List

from fastapi import Depends, HTTPException, status

from backend.api.skills.schemas import SkillsResponseSchema
from backend.api.companies.repository import get_company_by_id
from backend.api.vacancies.repository import get_vacancy_repo, get_vacancy_by_id
from backend.api.vacancies.schemas import VacancySchema, VacancyAddSchema, VacancyUpdateSchema
from backend.utils.auth_utils.token_dependencies import get_user_by_token
from backend.api.users.employers.dependencies import get_employer_by_token
from backend.api.users.employers.schemas import EmployerSchema
from backend.utils.auth_utils.check_func import check_employer_can_update
from backend.api.skills.repository import update_vacancy_skills


async def create_vacancy_dependencies(
        add_vacancy: VacancyAddSchema,
        owner: EmployerSchema = Depends(get_employer_by_token)
) -> Tuple[VacancySchema | None, EmployerSchema]:
    skills: List[SkillsResponseSchema] = add_vacancy.skills
    if not owner.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user dont have company'
        )
    vacancy_repo = get_vacancy_repo()
    vacancy = await vacancy_repo.add_one(company_id=owner.company_id, **add_vacancy.model_dump(exclude={'skills'}))
    await update_vacancy_skills(skills, vacancy.id)
    return vacancy, owner


async def get_vacancy_by_id_dependencies(
        vacancy_id: int,
        user=Depends(get_user_by_token)
) -> Tuple[VacancySchema, EmployerSchema, bool, str]:
    vacancy = await get_vacancy_by_id(vacancy_id)
    can_update = check_employer_can_update(user, vacancy)
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='vacancy is not exist'
        )
    company = await get_company_by_id(vacancy.company_id)
    return vacancy, user, can_update, company.name


async def delete_vacancy_by_id_dependencies(
        vacancy_id: int,
        owner: EmployerSchema = Depends(get_employer_by_token)
) -> Tuple[VacancySchema | None, EmployerSchema]:
    if not owner.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user dont have company'
        )
    vacancy_for_delete = await get_vacancy_by_id(vacancy_id)
    if owner.company_id != vacancy_for_delete.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user is not owner this company'
        )
    vacancy_repo = get_vacancy_repo()
    vacancy = await vacancy_repo.soft_delete(vacancy_id, 'delete')
    return vacancy, owner


async def update_vacancy_by_id_dependencies(
        vacancy_id: int,
        new_vacancy: VacancyUpdateSchema,
        owner: EmployerSchema = Depends(get_employer_by_token),
) -> Tuple[VacancySchema | None, EmployerSchema]:
    if not owner.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user dont have company'
        )
    vacancy_for_update = await get_vacancy_by_id(vacancy_id)
    if owner.company_id != vacancy_for_update.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user is not owner this company'
        )
    vacancy_repo = get_vacancy_repo()
    vacancy = await vacancy_repo.update_one(id=vacancy_id, **new_vacancy.model_dump())
    return vacancy, owner
