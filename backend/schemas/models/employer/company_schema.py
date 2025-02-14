from typing import List, Optional

from backend.schemas.global_schema import GlobalSchema
from backend.utils.str_const import COMPANY_TYPE


class CompanySchema(GlobalSchema):
    name: str
    description: str
    type: str = COMPANY_TYPE

    vacancies: Optional[List['VacancySchema']]



