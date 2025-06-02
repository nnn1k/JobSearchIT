from typing import Optional

from pydantic import ConfigDict, BaseModel

from backend.core.schemas.user_schema import UserResponseSchema
from backend.core.utils.const import EMPLOYER_USER_TYPE


class EmployerSchemaRel(UserResponseSchema):
    company_id: Optional[int] = None
    is_owner: bool = False
    type: str = EMPLOYER_USER_TYPE

    company: Optional['CompanySchemaRel'] = None


class EmployerSchema(UserResponseSchema):
    company_id: Optional[int] = None
    is_owner: bool = False

    type: str = EMPLOYER_USER_TYPE


class EmployerProfileSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    phone: Optional[str] = None
