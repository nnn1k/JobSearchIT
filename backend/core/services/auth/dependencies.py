from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.utils.dependencies import get_db
from backend.core.services.auth.repository import AuthRepository
from backend.core.services.auth.service import AuthService


def get_auth_repo(session: AsyncSession = Depends(get_db)):
    return AuthRepository(session=session)


def get_auth_serv(auth_repo: AuthRepository = Depends(get_auth_repo)):
    return AuthService(auth_repo=auth_repo)
