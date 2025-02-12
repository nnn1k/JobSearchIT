from typing import Tuple, List

from fastapi import Depends, HTTPException, status

from backend.api.vacancies.queries import (
    create_vacancy_queries,
    get_vacancy_by_id_queries,
    update_vacancy_by_id_queries
)
from backend.schemas.skill_schema import SkillsResponseSchema

from backend.api.vacancies.schemas import VacancyAddSchema, VacancyUpdateSchema
from backend.schemas import VacancySchema
from backend.utils.auth_utils.token_dependencies import get_user_by_token
from backend.api.users.employers.profile.dependencies import get_employer_by_token
from backend.schemas import EmployerResponseSchema
from backend.utils.auth_utils.check_func import check_employer_can_update
from backend.api.skills.queries import update_vacancy_skills
from backend.utils.other.time_utils import current_time
from backend.utils.other.type_utils import UserVar


async def create_vacancy_dependencies(
        add_vacancy: VacancyAddSchema,
        owner: EmployerResponseSchema = Depends(get_employer_by_token)
) -> Tuple[VacancySchema | None, EmployerResponseSchema]:
    skills: List[SkillsResponseSchema] = add_vacancy.skills
    if not owner.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user dont have company'
        )
    vacancy = await create_vacancy_queries(company_id=owner.company_id, **add_vacancy.model_dump(exclude={'skills'}))
    await update_vacancy_skills(skills, vacancy.id)
    return vacancy, owner


async def get_vacancy_by_id_dependencies(
        vacancy_id: int,
        user=Depends(get_user_by_token)
) -> Tuple[VacancySchema, UserVar, bool]:
    vacancy = await get_vacancy_by_id_queries(vacancy_id)
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='vacancy is not exist'
        )
    can_update = check_employer_can_update(user, vacancy)
    return vacancy, user, can_update


async def update_vacancy_by_id_dependencies(
        vacancy_id: int,
        new_vacancy: VacancyUpdateSchema,
        owner: EmployerResponseSchema = Depends(get_employer_by_token),
) -> Tuple[VacancySchema | None, EmployerResponseSchema]:
    vacancy = await update_vacancy_by_id_queries(vacancy_id, owner, **new_vacancy.model_dump())
    if vacancy is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user is not owner this company or vacancy not found'
        )
    return vacancy, owner


async def delete_vacancy_by_id_dependencies(
        vacancy_id: int,
        owner: EmployerResponseSchema = Depends(get_employer_by_token)
) -> Tuple[VacancySchema | None, EmployerResponseSchema]:
    deleted_at = current_time()
    vacancy = await update_vacancy_by_id_queries(vacancy_id, owner, deleted_at=deleted_at)
    if vacancy is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user is not owner this company or vacancy not found'
        )
    return vacancy, owner
