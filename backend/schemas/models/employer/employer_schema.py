from typing import Optional

from backend.schemas.user_schema import UserResponseSchema
from backend.utils.str_const import EMPLOYER_USER_TYPE


class EmployerResponseSchema(UserResponseSchema):
    company_id: Optional[int] = None
    is_owner: bool = False
    type: str = EMPLOYER_USER_TYPE

    company: Optional['CompanySchema'] = None




