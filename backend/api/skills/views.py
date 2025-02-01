from typing import List

from fastapi import APIRouter, Depends

from backend.api.skills.dependencies import (
    get_all_skills_dependencies,
    get_worker_skills_dependencies,
    get_vacancy_skills_dependencies
)
from backend.api.skills.schemas import SkillSchema

router = APIRouter(prefix="/skills", tags=["skills"])

@router.get('/', summary='Получить все скиллы')
def get_all_skills(
        skills_and_user: List[SkillSchema] = Depends(get_all_skills_dependencies)
):
    skills, user = skills_and_user
    return {
        'status': 'ok',
        'skills': skills,
        'user': user
    }


@router.get('/worker/me', summary='Вытащить все скиллы, которые привязаны к работнику')
def get_worker_skills_views(
        skills_and_user: List[SkillSchema] = Depends(get_worker_skills_dependencies)
):
    available_skills, worker_skills, user = skills_and_user
    return {
        'status': 'ok',
        'available_skills': available_skills,
        'worker_skills': worker_skills,
        'user': user
    }

@router.get('/vacancies/{vacancy_id}', summary='Вытащить все скиллы, которые привязаны к вакансии')
def get_vacancy_skills_views(
    skills_and_user: List[SkillSchema] = Depends(get_vacancy_skills_dependencies)
):
    available_skills, vacancy_skills, user = skills_and_user
    return {
        'status': 'ok',
        'available_skills': available_skills,
        'vacancy_skills': vacancy_skills,
        'user': user
    }