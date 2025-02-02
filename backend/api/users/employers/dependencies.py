from typing import Optional

from fastapi import Cookie, Depends

from backend.utils.auth_utils.token_dependencies import get_user_by_token_and_role
from backend.api.users.employers.repository import get_employer_repo
from backend.api.users.employers.schemas import EmployerSchema, EmployerProfileSchema, EmployerResponseSchema
from backend.api.users.profile_dependencies import user_patch_dependencies
from backend.schemas.global_schema import DynamicSchema, UserSchema


async def get_employer_by_token(
    access_token=Cookie(None),
) -> UserSchema:
    employer_repo = get_employer_repo()
    return await get_user_by_token_and_role(access_token, employer_repo, EmployerSchema, EmployerResponseSchema)


async def put_employer_dependencies(
        new_employer: EmployerProfileSchema,
        employer: EmployerSchema = Depends(get_employer_by_token)
) -> Optional[EmployerSchema]:
    employer_repo = get_employer_repo()
    return await employer_repo.update_one(id=employer.id, **new_employer.model_dump())


async def patch_employer_dependencies(
        new_employer: DynamicSchema,
        employer: EmployerSchema = Depends(get_employer_by_token)
) -> Optional[EmployerSchema]:
    employer_repo = get_employer_repo()
    return await user_patch_dependencies(employer, new_employer, employer_repo)
