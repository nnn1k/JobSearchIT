from fastapi import Depends

from backend.api.skills.repository import get_all_skills, get_available_skills, get_skills_by_worker_id
from backend.api.users.auth.token_dependencies import get_user_by_token
from backend.api.users.workers.dependencies import get_worker_by_token


async def get_all_skills_dependencies(
        user=Depends(get_user_by_token)
):
    skills = await get_all_skills()
    return skills, user

async def get_worker_skills_dependencies(
    user=Depends(get_worker_by_token)
):
    available_skills = await get_available_skills(user.id)
    worker_skills = await get_skills_by_worker_id(user.id)
    return available_skills, worker_skills, user
