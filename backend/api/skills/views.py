from fastapi import APIRouter, Depends

from backend.api.skills.queries import (
    get_all_skills_queries, get_available_skills_on_vacancy,
    get_available_skills_on_worker,
    get_skills_by_vacancy_id,
    get_skills_by_worker_id, update_vacancy_skills, update_worker_skills
)
from backend.schemas.models.other.skill_schema import SkillListSchema
from backend.utils.auth_utils.user_login_dependencies import get_user_by_token, get_worker_by_token

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get('/', summary='Получить все скиллы')
async def get_all_skills_views(
        user=Depends(get_user_by_token)
):
    skills = await get_all_skills_queries()
    return {
        'status': 'ok',
        'skills': skills,
        'user': user
    }


@router.get('/worker/me', summary='Вытащить все скиллы, которые привязаны к работнику')
async def get_worker_skills_views(
        user=Depends(get_worker_by_token)
):
    available_skills = await get_available_skills_on_worker(user.id)
    worker_skills = await get_skills_by_worker_id(user.id)

    return {
        'status': 'ok',
        'worker_skills': worker_skills,
        'available_skills': available_skills,
        'user': user
    }


@router.put('/worker/me', summary='Обновить скиллы работника')
async def update_worker_skills_views(
        skills: SkillListSchema,
        user=Depends(get_worker_by_token)
):
    await update_worker_skills(skills.skills, user.id)
    return {
        'status': 'ok',
        'worker_skills': skills.skills,
        'user': user
    }


@router.get('/vacancies/{vacancy_id}', summary='Вытащить все скиллы, которые привязаны к вакансии')
async def get_vacancy_skills_views(
        vacancy_id: int,
        user=Depends(get_user_by_token)
):
    available_skills = await get_available_skills_on_vacancy(vacancy_id)
    vacancy_skills = await get_skills_by_vacancy_id(vacancy_id)
    return {
        'status': 'ok',
        'vacancy_skills': vacancy_skills,
        'available_skills': available_skills,
        'user': user
    }

@router.put('/vacancies/{vacancy_id}', summary='Обновить скиллы вакансии')
async def update_vacancy_skills_views(
        vacancy_id: int,
        skills: SkillListSchema,
        user=Depends(get_user_by_token)
):
    await update_vacancy_skills(skills.skills, vacancy_id)
    return {
        'status': 'ok',
        'vacancy_skills': skills.skills,
        'user': user
    }