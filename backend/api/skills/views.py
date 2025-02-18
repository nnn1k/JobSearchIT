from fastapi import APIRouter, Depends

from backend.api.skills.queries import (
    get_all_skills_queries, get_available_skills_on_vacancy,
    get_available_skills_on_resume,
    get_skills_by_vacancy_id,
    get_skills_by_resume_id, update_vacancy_skills, update_resume_skills
)
from backend.schemas.models.other.skill_schema import SkillListSchema
from backend.utils.auth_utils.user_login_dependencies import get_user_by_token, get_worker_by_token
from backend.utils.other.time_utils import time_it_async

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get('/', summary='Получить все скиллы')
@time_it_async
async def get_all_skills_views(
        user=Depends(get_user_by_token)
):
    skills = await get_all_skills_queries()
    return {
        'status': 'ok',
        'skills': skills,
    }


@router.get('/resumes/{resume_id}', summary='Вытащить все навыки, которые привязаны к резюме')
@time_it_async
async def get_worker_skills_views(
        resume_id: int,
        user=Depends(get_user_by_token)
):
    available_skills = await get_available_skills_on_resume(resume_id)
    resume_skills = await get_skills_by_resume_id(resume_id)

    return {
        'status': 'ok',
        'resume_skills': resume_skills,
        'available_skills': available_skills,
    }


@router.put('/resumes/{resume_id}', summary='Обновить навыки резюме')
@time_it_async
async def update_worker_skills_views(
        resume_id: int,
        skills: SkillListSchema,
        user=Depends(get_user_by_token)
):
    await update_resume_skills(skills.skills, resume_id)
    return {
        'status': 'ok',
        'worker_skills': skills.skills,
    }


@router.get('/vacancies/{vacancy_id}', summary='Вытащить все навыки, которые привязаны к вакансии')
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
    }

@router.put('/vacancies/{vacancy_id}', summary='Обновить навыки вакансии')
async def update_vacancy_skills_views(
        vacancy_id: int,
        skills: SkillListSchema,
        user=Depends(get_user_by_token)
):
    await update_vacancy_skills(skills.skills, vacancy_id)
    return {
        'status': 'ok',
        'vacancy_skills': skills.skills,
    }
