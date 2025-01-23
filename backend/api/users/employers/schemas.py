from typing import Optional, Any

from pydantic import BaseModel, EmailStr

from backend.schemas.global_schema import GlobalSchema

class EmployerSchema(GlobalSchema):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    password: bytes
    company_id: Optional[int] = None
    is_owner: bool = False
    is_confirmed: bool = False

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

class EmployerUpdateSchema(BaseModel):
    key: str
    value: Any
