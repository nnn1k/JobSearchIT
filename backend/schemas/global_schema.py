import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class GlobalSchema(BaseModel):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]


class CodeSchema(BaseModel):
    code: str


class DynamicSchema(BaseModel):
    class Config:
        extra = 'allow'
