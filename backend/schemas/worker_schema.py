from datetime import date
from typing import Any, List, Optional

from backend.schemas.user_schema import UserResponseSchema
from backend.utils.str_const import WORKER_USER_TYPE


class WorkerResponseSchema(UserResponseSchema):
    birthday: Optional[date] = None
    city: Optional[str] = None
    type: str = WORKER_USER_TYPE

    resumes: Optional[List['ResumeSchema']] = None
    skills: Optional[List['SkillSchema']] = None
    educations: Optional[Any] = None

