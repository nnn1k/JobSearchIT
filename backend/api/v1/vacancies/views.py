from collections import Counter
from typing import List

from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.v1.skills.queries import update_vacancy_skills
from backend.api.v1.vacancies.queries import (
    get_all_vacancies_query,
)
from backend.api.v1.vacancies.schemas import VacancyAddSchema, VacancyUpdateSchema
from backend.core.database.utils.dependencies import get_db
from backend.core.schemas import EmployerSchema, SkillSchema

from backend.core.services.vacancies.dependencies import get_vacancy_serv
from backend.core.services.vacancies.service import VacancyService
from backend.core.utils.auth_utils.check_func import check_employer_can_update
from backend.core.utils.auth_utils.user_login_dependencies import get_employer_by_token, get_user_by_token

router = APIRouter(prefix="/vacancy", tags=["vacancy"])


@router.post('', summary='Создать вакансию')
async def create_new_vacancy(
        new_vacancy: VacancyAddSchema,
        bg: BackgroundTasks,
        employer: EmployerSchema = Depends(get_employer_by_token),
        vacancy_serv: VacancyService = Depends(get_vacancy_serv),
):
    skills: List[SkillSchema] = new_vacancy.skills

    vacancy = await vacancy_serv.create_vacancy(
        company_id=employer.company_id, employer=employer, new_vacancy=new_vacancy
    )
    bg.add_task(update_vacancy_skills, skills_list=skills, vacancy_id=vacancy.id, owner=employer)
    return {
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
        'vacancies': vacancies[(page - 1) * size:page * size],
    }


@router.get('/{vacancy_id}', summary='Посмотреть информацию о вакансии')
async def get_info_on_vacancy(
        vacancy_id: int,
        user=Depends(get_user_by_token),
        vacancy_serv: VacancyService = Depends(get_vacancy_serv),
):
    vacancy = await vacancy_serv.get_vacancy_rel(vacancy_id)
    can_update = check_employer_can_update(user, vacancy)
    return {
        'vacancy': vacancy,
        'can_update': can_update,
    }


@router.put('/{vacancy_id}', summary='Изменить вакансию')
async def update_info_on_company(
        vacancy_id: int,
        new_vacancy: VacancyUpdateSchema,
        employer: EmployerSchema = Depends(get_employer_by_token),
        vacancy_serv: VacancyService = Depends(get_vacancy_serv),
):
    vacancy = await vacancy_serv.update_vacancy(
        vacancy_id=vacancy_id,
        employer=employer,
        **new_vacancy.model_dump()
    )
    return {
        'vacancy': vacancy,
    }


@router.delete('/{vacancy_id}', summary='Удалить вакансию')
async def delete_info_on_vacancy(
        vacancy_id: int,
        employer: EmployerSchema = Depends(get_employer_by_token),
        vacancy_serv: VacancyService = Depends(get_vacancy_serv),
):
    await vacancy_serv.delete_vacancy(vacancy_id=vacancy_id, employer=employer)
    return {
        'status': 'ok',
    }
