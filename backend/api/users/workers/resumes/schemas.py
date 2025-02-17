from typing import Optional, List

from pydantic import BaseModel

from backend.schemas import SkillSchema


class ResumeAddSchema(BaseModel):
    title: str
    description: str
    salary_first: Optional[int] = None
    salary_second: Optional[int] = None
    city: Optional[str] = None
    skills: List[SkillSchema]


class ResumeUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary_first: Optional[int] = None
    salary_second: Optional[int] = None
    city: Optional[str] = None
