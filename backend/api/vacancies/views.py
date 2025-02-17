from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.skills.queries import update_vacancy_skills
from backend.api.vacancies.queries import (
    create_vacancy_queries,
    get_vacancy_by_id_queries,
    update_vacancy_by_id_queries
)
from backend.api.vacancies.schemas import VacancyAddSchema, VacancyUpdateSchema
from backend.schemas import EmployerResponseSchema
from backend.schemas.models.other.skill_schema import SkillSchema
from backend.utils.auth_utils.check_func import check_employer_can_update
from backend.utils.auth_utils.user_login_dependencies import get_employer_by_token, get_user_by_token
from backend.utils.other.time_utils import current_time

router = APIRouter(prefix="/vacancy", tags=["vacancy"])


@router.post('', summary='Создать вакансию')
async def create_new_vacancy(
        add_vacancy: VacancyAddSchema,
        user: EmployerResponseSchema = Depends(get_employer_by_token)
):
    skills: List[SkillSchema] = add_vacancy.skills
    if not user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user dont have company'
        )
    vacancy = await create_vacancy_queries(company_id=user.company_id, **add_vacancy.model_dump(exclude={'skills'}))
    await update_vacancy_skills(skills, vacancy.id)
    return {
        'status': 'ok',
        'vacancy': vacancy,
    }


@router.get('/{vacancy_id}', summary='Посмотреть информацию о вакансии')
async def get_info_on_vacancy(
        vacancy_id: int,
        user=Depends(get_user_by_token)
):
    vacancy = await get_vacancy_by_id_queries(vacancy_id)
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='vacancy is not exist'
        )
    can_update = check_employer_can_update(user, vacancy)

    return {
        'status': 'ok',
        'vacancy': vacancy,
        'can_update': can_update,
    }


@router.put('/{vacancy_id}', summary='Изменить вакансию')
async def update_info_on_company(
        vacancy_id: int,
        new_vacancy: VacancyUpdateSchema,
        user: EmployerResponseSchema = Depends(get_employer_by_token),
):
    vacancy = await update_vacancy_by_id_queries(vacancy_id, user, **new_vacancy.model_dump())
    if vacancy is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user is not owner this company or vacancy not found'
        )
    return {
        'vacancy': vacancy,
        'status': 'ok',
    }


@router.delete('/{vacancy_id}', summary='Удалить вакансию')
async def delete_info_on_company(
        vacancy_id: int,
        user: EmployerResponseSchema = Depends(get_employer_by_token)
):
    deleted_at = current_time()
    vacancy = await update_vacancy_by_id_queries(vacancy_id, user, deleted_at=deleted_at)
    if vacancy is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user is not owner this company or vacancy not found'
        )
    return {
        'status': 'ok',
    }
