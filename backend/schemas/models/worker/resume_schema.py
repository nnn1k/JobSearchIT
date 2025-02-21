from typing import List, Optional

from pydantic import ConfigDict

from backend.schemas.global_schema import GlobalSchema
from backend.utils.const import RESUME_TYPE

class ResumeSchema(GlobalSchema):
    description: str
    profession_id: int
    salary_first: Optional[int] = None
    salary_second: Optional[int] = None
    city: Optional[str] = None
    is_hidden: bool = False
    worker_id: int
    type: str = RESUME_TYPE

    worker: Optional['WorkerResponseSchema'] = None
    skills: Optional[List['SkillSchema']] = None
    profession: Optional['ProfessionSchema'] = None

    model_config = ConfigDict(from_attributes=True)

