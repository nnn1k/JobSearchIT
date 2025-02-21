from typing import List, Optional

from pydantic import ConfigDict

from backend.schemas.global_schema import GlobalSchema
from backend.utils.const import COMPANY_TYPE


class CompanySchema(GlobalSchema):
    name: str
    description: str
    type: str = COMPANY_TYPE

    vacancies: Optional[List['VacancySchema']]

    model_config = ConfigDict(from_attributes=True)



