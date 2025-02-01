from fastapi import Depends

from backend.api.skills.repository import get_all_skills
from backend.api.users.auth.token_dependencies import get_user_by_token


async def get_all_skills_dependencies(
        user=Depends(get_user_by_token)
):
    skills = await get_all_skills()
    return skills, user
