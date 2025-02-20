from typing import Optional, List

from pydantic import BaseModel

from backend.schemas import SkillSchema
from backend.schemas.global_schema import ValidateSalarySchema


class VacancyAddSchema(ValidateSalarySchema):
    description: str
    city: Optional[str]
    skills: List[SkillSchema]


class VacancyUpdateSchema(ValidateSalarySchema):
    description: str
    city: str

