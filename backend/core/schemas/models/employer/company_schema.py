from typing import List, Optional

from pydantic import ConfigDict

from backend.core.schemas.global_schema import GlobalSchema
from backend.core.utils.const import COMPANY_TYPE


class CompanySchema(GlobalSchema):
    name: str
    description: Optional[str] = ''
    type: str = COMPANY_TYPE

    vacancies: Optional[List['VacancySchema']]

    model_config = ConfigDict(from_attributes=True)



