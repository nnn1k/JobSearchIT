from typing import List

from fastapi import APIRouter, Depends

from backend.api.skills.schemas import SkillSchema

router = APIRouter(prefix="/skills", tags=["skills"])

@router.get('/')
def get_all_skills(
        skills: List[SkillSchema] = Depends(get_all_skills)
):
    return {
        'status': 'ok',
        'skills': skills
    }
