from typing import Optional, List

from pydantic import BaseModel

from backend.schemas import SkillSchema


class VacancyAddSchema(BaseModel):
    title: str
    description: str
    salary_first: Optional[int]
    salary_second: Optional[int]
    city: Optional[str]
    skills: List[SkillSchema]

class VacancyUpdateSchema(BaseModel):
    title: str
    description: str
    salary_first: Optional[int]
    salary_second: Optional[int]
    city: str

