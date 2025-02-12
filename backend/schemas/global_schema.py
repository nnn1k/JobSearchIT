import datetime
from typing import Optional

from pydantic import BaseModel


class GlobalSchema(BaseModel):
    id: Optional[int]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]


class DynamicSchema(BaseModel):
    class Config:
        extra = 'allow'
