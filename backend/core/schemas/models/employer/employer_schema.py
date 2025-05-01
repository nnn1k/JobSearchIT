from typing import Optional

from pydantic import ConfigDict

from backend.core.schemas.user_schema import UserResponseSchema
from backend.core.utils.const import EMPLOYER_USER_TYPE


class EmployerSchemaRel(UserResponseSchema):
    company_id: Optional[int] = None
    is_owner: bool = False
    type: str = EMPLOYER_USER_TYPE

    company: Optional['CompanySchema'] = None


class EmployerSchema(UserResponseSchema):
    company_id: Optional[int] = None
    is_owner: bool = False

    type: str = EMPLOYER_USER_TYPE
