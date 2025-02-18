from typing import Optional, List

from pydantic import BaseModel

from backend.schemas import SkillSchema
from backend.schemas.global_schema import ValidateSalarySchema


class VacancyAddSchema(ValidateSalarySchema):
    title: str
    description: str
    city: Optional[str]
    skills: List[SkillSchema]


class VacancyUpdateSchema(ValidateSalarySchema):
    title: str
    description: str
    city: str

