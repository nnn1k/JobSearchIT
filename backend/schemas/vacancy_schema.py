from typing import List, Optional

from backend.schemas.global_schema import GlobalSchema


class VacancySchema(GlobalSchema):
    title: str
    description: str
    salary_first: Optional[int]
    salary_second: Optional[int]
    city: str
    company_id: int

    company: Optional['CompanySchema']
    skills: Optional[List['SkillSchema']]
