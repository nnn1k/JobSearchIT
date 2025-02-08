from typing import Optional, List

from pydantic import BaseModel

from backend.schemas.global_schema import GlobalSchema
from backend.api.skills.schemas import SkillsResponseSchema


class VacancySchema(GlobalSchema):
    title: str
    description: str
    salary_first: Optional[int]
    salary_second: Optional[int]
    city: str
    company_id: int


class VacancyAddSchema(BaseModel):
    title: str
    description: str
    salary_first: Optional[int]
    salary_second: Optional[int]
    city: Optional[str]
    skills: List[SkillsResponseSchema]

class VacancyUpdateSchema(BaseModel):
    title: str
    description: str
    salary_first: Optional[int]
    salary_second: Optional[int]
    city: str

