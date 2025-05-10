from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.utils.dependencies import get_db
from backend.core.services.users.repository import UserRepository
from backend.core.services.users.service import UserService


def get_user_repo(session: AsyncSession = Depends(get_db)):
    return UserRepository(session=session)


def get_user_serv(user_repo: UserRepository = Depends(get_user_repo)):
    return UserService(user_repo=user_repo)
