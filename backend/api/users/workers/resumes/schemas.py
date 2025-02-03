from typing import Optional, List, Any

from pydantic import BaseModel

from backend.api.skills.schemas import SkillsResponseSchema
from backend.schemas.global_schema import GlobalSchema


class ResumeSchema(GlobalSchema):
    title: str
    description: str
    salary_first: Optional[int] = None
    salary_second: Optional[int] = None
    city: Optional[str] = None
    is_hidden: bool = False
    worker_id: int


class ResumeAddSchema(BaseModel):
    title: str
    description: str
    salary_first: Optional[int] = None
    salary_second: Optional[int] = None
    city: Optional[str] = None
    skills: List[SkillsResponseSchema]


class ResumeUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary_first: Optional[int] = None
    salary_second: Optional[int] = None
