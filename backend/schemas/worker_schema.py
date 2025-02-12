from datetime import date
from typing import Any, List, Optional

from backend.schemas.user_schema import UserResponseSchema


class WorkerResponseSchema(UserResponseSchema):
    birthday: Optional[date] = None
    city: Optional[str] = None
    type: str = 'worker'

    resumes: Optional[List['ResumeSchema']] = None
    skills: Optional[List['SkillSchema']] = None
    educations: Optional[Any] = None

