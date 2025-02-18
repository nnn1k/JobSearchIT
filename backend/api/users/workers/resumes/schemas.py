from typing import Optional, List

from pydantic import BaseModel

from backend.schemas import SkillSchema
from backend.schemas.global_schema import ValidateSalarySchema


class ResumeAddSchema(ValidateSalarySchema):
    title: str
    description: str
    city: Optional[str] = None
    skills: List[SkillSchema]


class ResumeUpdateSchema(ValidateSalarySchema):
    title: Optional[str] = None
    description: Optional[str] = None
    city: Optional[str] = None
