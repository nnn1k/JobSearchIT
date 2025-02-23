from collections import Counter
from typing import List

from fastapi import APIRouter, Depends

from backend.api.skills.queries import update_vacancy_skills
from backend.api.vacancies.queries import (
    create_vacancy_queries,
    delete_vacancy_by_id_queries, get_all_vacancies_query, get_vacancy_by_id_queries,
    update_vacancy_by_id_queries
)
from backend.api.vacancies.schemas import VacancyAddSchema, VacancyUpdateSchema
from backend.schemas import EmployerResponseSchema
from backend.schemas.models.other.skill_schema import SkillSchema
from backend.utils.auth_utils.check_func import check_employer_can_update
from backend.utils.auth_utils.user_login_dependencies import get_employer_by_token, get_user_by_token
from backend.utils.other.time_utils import time_it_async

router = APIRouter(prefix="/vacancy", tags=["vacancy"])


@router.post('', summary='Создать вакансию')
@time_it_async
async def create_new_vacancy(
        add_vacancy: VacancyAddSchema,
        user: EmployerResponseSchema = Depends(get_employer_by_token)
):
    skills: List[SkillSchema] = add_vacancy.skills
    vacancy = await create_vacancy_queries(company_id=user.company_id, user=user, **add_vacancy.model_dump(exclude={'skills'}))
    await update_vacancy_skills(skills, vacancy.id, user)
    return {
        'status': 'ok',
        'vacancy': vacancy,
    }

@router.get('', summary='Поиск по вакансиям')
@time_it_async
async def get_vacancies(
        user=Depends(get_user_by_token),
        min_salary: int = None,
        have_salary: bool = None,
        profession: str = None,
        city: str = None,
):
    vacancies = await get_all_vacancies_query(
        user,
        min_salary=min_salary,
        have_salary=have_salary,
        profession=profession,
        city=city
    )
    cities = Counter(vacancy.city for vacancy in vacancies)
    return {
        'length': len(vacancies),
        'cities': cities,
        'status': 'ok',
        'vacancies': vacancies,
    }


@router.get('/{vacancy_id}', summary='Посмотреть информацию о вакансии')
@time_it_async
async def get_info_on_vacancy(
        vacancy_id: int,
        user=Depends(get_user_by_token)
):
    vacancy = await get_vacancy_by_id_queries(vacancy_id)
    can_update = check_employer_can_update(user, vacancy)
    return {
        'status': 'ok',
        'vacancy': vacancy,
        'can_update': can_update,
    }


@router.put('/{vacancy_id}', summary='Изменить вакансию')
@time_it_async
async def update_info_on_company(
        vacancy_id: int,
        new_vacancy: VacancyUpdateSchema,
        user: EmployerResponseSchema = Depends(get_employer_by_token),
):
    vacancy = await update_vacancy_by_id_queries(vacancy_id, user, **new_vacancy.model_dump())
    return {
        'vacancy': vacancy,
        'status': 'ok',
    }


@router.delete('/{vacancy_id}', summary='Удалить вакансию')
@time_it_async
async def delete_info_on_vacancy(
        vacancy_id: int,
        user: EmployerResponseSchema = Depends(get_employer_by_token)
):
    await delete_vacancy_by_id_queries(vacancy_id, user)
    return {
        'status': 'ok',
    }
