import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class GlobalSchema(BaseModel):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]


class CodeSchema(BaseModel):
    code: str


class UserTypeSchema(BaseModel):
    id: int
    type: str

class UserSchema(GlobalSchema):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    password: bytes
    is_confirmed: bool = False

class DynamicSchema(BaseModel):
    class Config:
        extra = 'allow'
