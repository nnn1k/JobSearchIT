from typing import Optional

from fastapi import Cookie, Depends

from backend.api.users.employers.profile.queries import update_employer_by_id_queries
from backend.utils.auth_utils.token_dependencies import get_user_by_token_and_role
from backend.api.users.employers.profile.schemas import EmployerProfileSchema
from backend.schemas import EmployerResponseSchema
from backend.schemas.global_schema import DynamicSchema


async def get_employer_by_token(
    access_token=Cookie(None),
) -> EmployerResponseSchema:
    return await get_user_by_token_and_role(access_token, 'employer')


async def put_employer_dependencies(
        new_employer: EmployerProfileSchema,
        employer: EmployerResponseSchema = Depends(get_employer_by_token)
) -> Optional[EmployerResponseSchema]:
    return await update_employer_by_id_queries(employer_id=employer.id, **new_employer.model_dump())


async def patch_employer_dependencies(
        new_employer: DynamicSchema,
        employer: EmployerResponseSchema = Depends(get_employer_by_token)
) -> Optional[EmployerResponseSchema]:
    return await update_employer_by_id_queries(employer_id=employer.id, **new_employer.model_dump())
