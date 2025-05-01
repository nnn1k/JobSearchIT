from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.utils.dependencies import get_db
from backend.core.services.professions.repository import ProfessionRepository
from backend.core.services.professions.service import ProfessionService


def get_prof_repo(session: AsyncSession = Depends(get_db)):
    return ProfessionRepository(session=session)


def get_prof_serv(prof_repo: ProfessionRepository = Depends(get_prof_repo)):
    return ProfessionService(prof_repo=prof_repo)
