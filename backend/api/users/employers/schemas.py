from typing import Optional, Any

from pydantic import BaseModel, EmailStr

from backend.schemas.global_schema import UserSchema


class EmployerSchema(UserSchema):
    company_id: Optional[int] = None
    is_owner: bool = False


class EmployerAuthSchema(BaseModel):
    email: EmailStr
    password: str


class EmployerRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

class EmployerProfileSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    phone: Optional[str] = None

