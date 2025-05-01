from typing import List, Optional

from backend.core.schemas.global_schema import GlobalSchema
from backend.core.utils.const import VACANCY_TYPE


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
