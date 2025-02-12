from typing import List, Optional

from backend.schemas.global_schema import GlobalSchema


class CompanySchema(GlobalSchema):
    name: str
    description: str

    vacancies: Optional[List['VacancySchema']]



