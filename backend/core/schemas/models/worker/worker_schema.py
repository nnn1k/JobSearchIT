from datetime import date
from typing import Any, List, Optional

from pydantic import ConfigDict, BaseModel

from backend.core.schemas.user_schema import UserResponseSchema
from backend.core.utils.const import WORKER_USER_TYPE


class WorkerSchemaRel(UserResponseSchema):
    birthday: Optional[date] = None
    city: Optional[str] = None
    type: str = WORKER_USER_TYPE

    resumes: Optional[List['ResumeSchema']] = None

    model_config = ConfigDict(from_attributes=True)


class WorkerSchema(UserResponseSchema):
    birthday: Optional[date] = None
    city: Optional[str] = None

    type: str = WORKER_USER_TYPE


class WorkerProfileSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    city: Optional[str] = None
