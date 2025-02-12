from typing import Optional, List

from pydantic import BaseModel

from backend.schemas.skill_schema import SkillsResponseSchema


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

