from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr

from backend.schemas.global_schema import UserSchema, UserResponseSchema


class WorkerSchema(UserSchema):
    birthday: Optional[date] = None
    city: Optional[str] = None


class WorkerResponseSchema(UserResponseSchema):
    birthday: Optional[date] = None
    city: Optional[str] = None
    type: str = 'worker'


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
    city: Optional[str] = None
