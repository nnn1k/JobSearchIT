from typing import Optional

from fastapi import Cookie, Depends

from backend.utils.auth_utils.token_dependencies import get_user_by_token_and_role
from backend.api.users.employers.profile.repository import get_employer_repo
from backend.api.users.employers.profile.schemas import EmployerProfileSchema, EmployerResponseSchema
from backend.api.users.profile_dependencies import user_patch_dependencies
from backend.schemas.global_schema import DynamicSchema


async def get_employer_by_token(
    access_token=Cookie(None),
) -> EmployerResponseSchema:
    employer_repo = get_employer_repo()
    return await get_user_by_token_and_role(access_token, employer_repo)


async def put_employer_dependencies(
        new_employer: EmployerProfileSchema,
        employer: EmployerResponseSchema = Depends(get_employer_by_token)
) -> Optional[EmployerResponseSchema]:
    employer_repo = get_employer_repo()
    return await employer_repo.update_one(id=employer.id, **new_employer.model_dump())


async def patch_employer_dependencies(
        new_employer: DynamicSchema,
        employer: EmployerResponseSchema = Depends(get_employer_by_token)
) -> Optional[EmployerResponseSchema]:
    employer_repo = get_employer_repo()
    return await user_patch_dependencies(employer, new_employer, employer_repo)
