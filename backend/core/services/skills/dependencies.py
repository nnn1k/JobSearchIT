from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.utils.dependencies import get_db
from backend.core.services.skills.repository import SkillRepository
from backend.core.services.skills.service import SkillService


def get_skill_repo(session: AsyncSession = Depends(get_db)):
    return SkillRepository(session=session)


def get_skill_serv(skill_repo: SkillRepository = Depends(get_skill_repo)):
    return SkillService(skill_repo=skill_repo)
