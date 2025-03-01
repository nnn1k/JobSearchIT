from typing import Optional, List

from pydantic import BaseModel, Field

from backend.schemas import SkillSchema
from backend.schemas.global_schema import ValidateSalarySchema


class ResumeAddSchema(ValidateSalarySchema):
    description: str
    city: Optional[str] = None
    skills: List[SkillSchema]


class ResumeUpdateSchema(ValidateSalarySchema):
    description: Optional[str] = None
    city: Optional[str] = None
