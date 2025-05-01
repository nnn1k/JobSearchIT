from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr
from enum import Enum

from backend.core.schemas.user_schema import UserResponseSchema
from backend.core.utils.const import WORKER_USER_TYPE, EMPLOYER_USER_TYPE


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str


class WorkerSchema(UserResponseSchema):
    birthday: Optional[date] = None
    city: Optional[str] = None

    type: str = WORKER_USER_TYPE


class EmployerSchema(UserResponseSchema):
    company_id: Optional[int] = None
    is_owner: bool = False

    type: str = EMPLOYER_USER_TYPE


