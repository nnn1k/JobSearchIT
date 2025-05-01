from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.utils.dependencies import get_db
from backend.core.services.responses.repository import ResponseRepository
from backend.core.services.responses.service import ResponseService


def get_resp_repo(session: AsyncSession = Depends(get_db)):
    return ResponseRepository(session=session)


def get_resp_serv(resp_repo: ResponseRepository = Depends(get_resp_repo)):
    return ResponseService(resp_repo=resp_repo)
