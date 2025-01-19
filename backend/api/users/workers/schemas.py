from datetime import date
from typing import Optional, Any

from pydantic import BaseModel, EmailStr

from backend.schemas.global_schema import GlobalSchema


class WorkerSchema(GlobalSchema):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    password: bytes
    birthday: Optional[date] = None
    gender: Optional[str]
    city: Optional[str] = None
    is_confirmed: bool = False


class WorkerAuthSchema(BaseModel):
    email: EmailStr
    password: str


class WorkerRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

class WorkerProfileSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    gender: Optional[str] = None
    city: Optional[str] = None

class WorkerUpdateSchema(BaseModel):
    key: str
    value: Any
