from typing import Optional

from pydantic import BaseModel

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
    salary_first: Optional[str] = None
    salary_second: Optional[str] = None

class ResumeUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary_first: Optional[str] = None
    salary_second: Optional[str] = None
