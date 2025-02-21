from typing import List, Optional

from pydantic import ConfigDict

from backend.schemas.global_schema import GlobalSchema
from backend.utils.str_const import VACANCY_TYPE


class VacancySchema(GlobalSchema):
    title: str
    description: str
    salary_first: Optional[int]
    salary_second: Optional[int]
    city: str
    company_id: int
    type: str = VACANCY_TYPE

    company: Optional['CompanySchema']
    skills: Optional[List['SkillSchema']]

    model_config = ConfigDict(from_attributes=True)