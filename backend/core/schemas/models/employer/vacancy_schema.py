from typing import List, Optional

from pydantic import model_validator

from backend.core.schemas.global_schema import GlobalSchema, ValidateSalarySchema
from backend.core.schemas.models.other.skill_schema import SkillSchema
from backend.core.utils.const import VACANCY_TYPE, WORKER_USER_TYPE, EMPLOYER_USER_TYPE


class VacancySchema(GlobalSchema):
    description: str
    salary_first: Optional[int]
    salary_second: Optional[int]
    city: str
    company_id: int
    type: str = VACANCY_TYPE


class VacancySchemaRel(VacancySchema):
    company: Optional['CompanySchema']
    skills: Optional[List['SkillSchema']]
    profession: Optional['ProfessionSchema'] = None
    responses: Optional[List['ResponseSchema']] = None
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


class VacancyAddSchema(ValidateSalarySchema):
    description: str
    city: Optional[str] = None
    skills: List[SkillSchema]


class VacancyUpdateSchema(ValidateSalarySchema):
    description: str
    city: str
