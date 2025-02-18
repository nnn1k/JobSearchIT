from typing import List, Optional

from pydantic import ConfigDict, validator

from backend.schemas.global_schema import GlobalSchema
from backend.utils.str_const import RESUME_TYPE
from fastapi import status, HTTPException

class ResumeSchema(GlobalSchema):
    title: str
    description: str
    salary_first: Optional[int] = None
    salary_second: Optional[int] = None
    city: Optional[str] = None
    is_hidden: bool = False
    worker_id: int
    type: str = RESUME_TYPE

    worker: Optional['WorkerResponseSchema'] = None
    skills: Optional[List['SkillSchema']] = None

    model_config = ConfigDict(from_attributes=True)

