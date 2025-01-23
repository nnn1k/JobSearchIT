from fastapi import Depends, HTTPException, status

from backend.api.users.auth.auth_dependencies import register_user, login_user
from backend.api.users.employers.dependencies import get_employer_by_token
from backend.api.users.employers.repository import get_employer_repo
from backend.api.users.employers.schemas import EmployerAuthSchema, EmployerSchema, EmployerRegisterSchema
from backend.schemas.global_schema import CodeSchema
from backend.utils.other.email_func import send_code_to_email
from backend.utils.other.redis_func import get_code_from_redis


async def login_employer_dependencies(
    log_user: EmployerAuthSchema
) -> EmployerSchema:
    employer_repo = get_employer_repo()
    return await login_user(log_user, employer_repo)


async def register_employer_dependencies(
        reg_user: EmployerRegisterSchema,
) -> EmployerSchema:
    employer_repo = get_employer_repo()

    return await register_user(reg_user, employer_repo)

async def get_code_dependencies(
        employer: EmployerSchema = Depends(get_employer_by_token),
):
    send_code_to_email(employer, 'employer')
    return employer

async def check_code_dependencies(
        code: CodeSchema,
        employer: EmployerSchema = Depends(get_employer_by_token),
):
    new_code = get_code_from_redis('employer', employer.id)
    if code.code == new_code:
        employer_repo = get_employer_repo()
        return await employer_repo.update_one(id=employer.id, is_confirmed=True)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect code",
    )


