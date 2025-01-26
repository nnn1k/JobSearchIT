from fastapi import Depends

from backend.api.users.auth.auth_dependencies import register_user, login_user, check_user_code_dependencies
from backend.api.users.employers.dependencies import get_employer_by_token
from backend.api.users.employers.repository import get_employer_repo
from backend.api.users.employers.schemas import EmployerAuthSchema, EmployerSchema, EmployerRegisterSchema
from backend.schemas.global_schema import CodeSchema
from backend.utils.other.email_func import SendEmail


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
) -> EmployerSchema:
    SendEmail.send_code_to_email(employer, 'employer')
    return employer

async def check_code_dependencies(
        code: CodeSchema,
        employer: EmployerSchema = Depends(get_employer_by_token),
) -> EmployerSchema:
    employer_repo = get_employer_repo()
    return await check_user_code_dependencies(employer, employer_repo, code)
