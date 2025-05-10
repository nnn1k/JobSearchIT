from fastapi import Depends

from backend.core.services.users.dependencies import get_user_repo
from backend.core.services.users.repository import UserRepository
from backend.core.services.auth.service import AuthService


def get_auth_serv(user_serv: UserRepository = Depends(get_user_repo)):
    return AuthService(user_repo=user_serv)
