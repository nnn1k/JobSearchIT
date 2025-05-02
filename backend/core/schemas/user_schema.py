from typing import Literal, Optional

from pydantic import BaseModel, EmailStr

from backend.core.schemas.global_schema import GlobalSchema


class UserTypeSchema(BaseModel):
    id: int
    type: str


class UserResponseSchema(GlobalSchema):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    is_confirmed: Optional[bool] = False


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
