from typing import Optional

from pydantic import BaseModel

from backend.schemas.user_schema import UserResponseSchema, UserSchema


class EmployerSchema(UserSchema):
    company_id: Optional[int] = None
    is_owner: bool = False


class EmployerResponseSchema(UserResponseSchema):
    company_id: Optional[int] = None
    is_owner: bool = False
    type: str = 'employer'


class EmployerProfileSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    phone: Optional[str] = None
