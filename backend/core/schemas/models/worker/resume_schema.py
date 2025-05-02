from typing import List, Optional


from backend.core.schemas.global_schema import GlobalSchema, ValidateSalarySchema
from backend.core.utils.const import RESUME_TYPE


class ResumeSchema(GlobalSchema):
    description: str
    profession_id: int
    salary_first: Optional[int] = None
    salary_second: Optional[int] = None
    city: Optional[str] = None
    is_hidden: bool = False
    worker_id: int
    type: str = RESUME_TYPE


class ResumeSchemaRel(ResumeSchema):
    worker: Optional['WorkerSchema'] = None
    skills: Optional[List['SkillSchema']] = None
    profession: Optional['ProfessionSchema'] = None


class ResumeAddSchema(ValidateSalarySchema):
    description: str
    city: Optional[str] = None
    skills: List['SkillSchema']


class ResumeUpdateSchema(ValidateSalarySchema):
    description: Optional[str] = None
    city: Optional[str] = None
