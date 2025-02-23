from typing import Optional

from pydantic import ConfigDict

from backend.schemas.user_schema import UserResponseSchema
from backend.utils.const import EMPLOYER_USER_TYPE


class EmployerResponseSchema(UserResponseSchema):
    company_id: Optional[int] = None
    is_owner: bool = False
    type: str = EMPLOYER_USER_TYPE

    company: Optional['CompanySchema'] = None

    model_config = ConfigDict(from_attributes=True)


