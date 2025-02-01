from typing import List

from fastapi import APIRouter, Depends

from backend.api.skills.dependencies import get_all_skills_dependencies
from backend.api.skills.schemas import SkillSchema

router = APIRouter(prefix="/skills", tags=["skills"])

@router.get('/')
def get_all_skills(
        skills_and_user: List[SkillSchema] = Depends(get_all_skills_dependencies)
):
    skills, user = skills_and_user
    return {
        'status': 'ok',
        'skills': skills,
        'user': user
    }
