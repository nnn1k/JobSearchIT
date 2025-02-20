from typing import Optional, List

from pydantic import BaseModel, Field

from backend.schemas import SkillSchema
from backend.schemas.global_schema import ValidateSalarySchema


class ResumeAddSchema(ValidateSalarySchema):
    profession_id: int
    description: str
    city: Optional[str] = None
    skills: List[SkillSchema]


class ResumeUpdateSchema(ValidateSalarySchema):
    profession_id: int
    description: Optional[str] = None
    city: Optional[str] = None
