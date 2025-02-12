from fastapi import Depends

from backend.api.skills.queries import (
    get_all_skills,
    get_available_skills_on_worker,
    get_skills_by_worker_id,
    get_available_skills_on_vacancy, get_skills_by_vacancy_id
)
from backend.utils.auth_utils.token_dependencies import get_user_by_token
from backend.api.users.workers.profile.dependencies import get_worker_by_token


async def get_all_skills_dependencies(
        user=Depends(get_user_by_token)
):
    skills = await get_all_skills()
    return skills, user

async def get_worker_skills_dependencies(
    user=Depends(get_worker_by_token)
):
    available_skills = await get_available_skills_on_worker(user.id)
    worker_skills = await get_skills_by_worker_id(user.id)
    return available_skills, worker_skills, user

async def get_vacancy_skills_dependencies(
        vacancy_id: int,
        user=Depends(get_user_by_token)
):
    available_skills = await get_available_skills_on_vacancy(vacancy_id)
    vacancy_skills = await get_skills_by_vacancy_id(vacancy_id)
    return available_skills, vacancy_skills, user
