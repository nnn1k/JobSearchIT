from typing import Optional, List

from backend.core.schemas import SkillSchema
from backend.core.schemas.global_schema import ValidateSalarySchema


class VacancyAddSchema(ValidateSalarySchema):
    description: str
    city: Optional[str]
    skills: List[SkillSchema]


class VacancyUpdateSchema(ValidateSalarySchema):
    description: str
    city: str

