from typing import Literal, Optional

from pydantic import BaseModel, EmailStr

from backend.core.schemas.global_schema import GlobalSchema


class UserTypeSchema(BaseModel):
    id: int
    type: str


class UserAbstractSchema(GlobalSchema):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    is_confirmed: Optional[bool] = False


class UserSchema(UserAbstractSchema):
    password: bytes


class UserResponseSchema(UserAbstractSchema):
    type: Literal['worker', 'employer']
