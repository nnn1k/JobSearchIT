from typing import List, Optional

from pydantic import model_validator

from backend.core.schemas.global_schema import GlobalSchema, ValidateSalarySchema
from backend.core.utils.const import RESUME_TYPE, WORKER_USER_TYPE, EMPLOYER_USER_TYPE


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
    responses: Optional[List['ResponseSchema']] = []
    response_count: int = 0
    invite_count: int = 0

    @model_validator(mode='after')
    def count_responses_and_invites(self) -> 'ResumeSchemaRel':
        if self.responses:
            for response in self.responses:
                if response.first == WORKER_USER_TYPE:
                    self.response_count += 1
                elif response.first == EMPLOYER_USER_TYPE:
                    self.invite_count += 1
        return self



class ResumeAddSchema(ValidateSalarySchema):
    description: str
    city: Optional[str] = None
    skills: List['SkillSchema']


class ResumeUpdateSchema(ValidateSalarySchema):
    description: Optional[str] = None
    city: Optional[str] = None
