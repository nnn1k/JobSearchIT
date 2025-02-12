from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr
from enum import Enum

from backend.schemas.user_schema import UserSchema


class UserType(str, Enum):
    worker: str = "workers"
    employer: str = "employers"

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

class WorkerSchema(UserSchema):
    birthday: Optional[date] = None
    city: Optional[str] = None

class EmployerSchema(UserSchema):
    company_id: Optional[int] = None
    is_owner: bool = False


class CodeSchema(BaseModel):
    code: str
