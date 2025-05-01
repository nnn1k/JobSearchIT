from typing import List, Optional

from pydantic import ConfigDict

from backend.core.schemas.global_schema import GlobalSchema
from backend.core.utils.const import COMPANY_TYPE


class CompanySchema(GlobalSchema):
    name: str
    description: Optional[str] = ''
    type: str = COMPANY_TYPE


class CompanySchemaRel(CompanySchema):
    vacancies: Optional[List['VacancySchema']]



