from fastapi import Cookie

from backend.api.users.auth.token_dependencies import get_user_by_token
from backend.api.users.employers.repository import get_employer_repo
from backend.api.users.employers.schemas import EmployerSchema


async def get_employer_by_token(
    access_token=Cookie(None),
) -> EmployerSchema:
    employer_repo = get_employer_repo()
    return await get_user_by_token(access_token, employer_repo, EmployerSchema)
