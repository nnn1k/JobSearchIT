from collections import Counter
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.skills.queries import update_vacancy_skills
from backend.api.vacancies.queries import (
    create_vacancy_queries,
    delete_vacancy_by_id_queries,
    get_all_vacancies_query,
    get_vacancy_by_id_queries,
    update_vacancy_by_id_queries
)
from backend.api.vacancies.schemas import VacancyAddSchema, VacancyUpdateSchema
from backend.core.database.utils.dependencies import get_db
from backend.core.schemas import EmployerResponseSchema
from backend.core.schemas import SkillSchema
from backend.core.utils.auth_utils.check_func import check_employer_can_update
from backend.core.utils.auth_utils.user_login_dependencies import get_employer_by_token, get_user_by_token

router = APIRouter(prefix="/vacancy", tags=["vacancy"])


@router.post('', summary='Создать вакансию')
async def create_new_vacancy(
        add_vacancy: VacancyAddSchema,
        user: EmployerResponseSchema = Depends(get_employer_by_token),
        session: AsyncSession = Depends(get_db),
):
    skills: List[SkillSchema] = add_vacancy.skills
    vacancy = await create_vacancy_queries(
        company_id=user.company_id,
        user=user,
        session=session,
        **add_vacancy.model_dump(exclude={'skills'})
    )
    await update_vacancy_skills(skills, vacancy.id, user)
    return {
        'status': 'ok',
        'vacancy': vacancy,
    }

@router.get('', summary='Поиск по вакансиям')
async def get_vacancies(
        user=Depends(get_user_by_token),
        min_salary: int = Query(None, ge=0),
        profession: str = None,
        city: str = None,
        page: int = Query(1, gt=0),
        size: int = Query(10, ge=0),
        session: AsyncSession = Depends(get_db),
):
    vacancies, params = await get_all_vacancies_query(
        user=user,
        session=session,
        min_salary=min_salary,
        profession=profession,
        city=city,
    )
    cities = Counter(vacancy.city for vacancy in vacancies)
    user_type = user.type if user else None
    return {
        'params': params,
        'count': len(vacancies),
        'user_type': user_type,
        'cities': cities,
        'status': 'ok',
        'vacancies': vacancies[(page - 1) * size:page * size],
    }


@router.get('/{vacancy_id}', summary='Посмотреть информацию о вакансии')
async def get_info_on_vacancy(
        vacancy_id: int,
        user=Depends(get_user_by_token),
        session: AsyncSession = Depends(get_db),
):
    vacancy = await get_vacancy_by_id_queries(vacancy_id, session)
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
        session: AsyncSession = Depends(get_db),
):
    vacancy = await update_vacancy_by_id_queries(vacancy_id, user, session, **new_vacancy.model_dump())
    return {
        'vacancy': vacancy,
        'status': 'ok',
    }


@router.delete('/{vacancy_id}', summary='Удалить вакансию')
async def delete_info_on_vacancy(
        vacancy_id: int,
        user: EmployerResponseSchema = Depends(get_employer_by_token),
        session: AsyncSession = Depends(get_db),
):
    await delete_vacancy_by_id_queries(vacancy_id, user, session)
    return {
        'status': 'ok',
    }

