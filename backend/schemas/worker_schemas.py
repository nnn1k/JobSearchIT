from datetime import date
from typing import Optional

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