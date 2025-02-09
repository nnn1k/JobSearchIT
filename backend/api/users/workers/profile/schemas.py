from datetime import date
from typing import Optional

from pydantic import BaseModel

from backend.schemas.user_schema import UserResponseSchema, UserSchema


class WorkerSchema(UserSchema):
    birthday: Optional[date] = None
    city: Optional[str] = None


class WorkerResponseSchema(UserResponseSchema):
    birthday: Optional[date] = None
    city: Optional[str] = None
    type: str = 'worker'


class WorkerProfileSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    city: Optional[str] = None
