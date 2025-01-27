import datetime
from typing import Optional

from pydantic import BaseModel


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


class DynamicSchema(BaseModel):
    class Config:
        extra = 'allow'
