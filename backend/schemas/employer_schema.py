from typing import Optional

from backend.schemas.user_schema import UserResponseSchema


class EmployerResponseSchema(UserResponseSchema):
    company_id: Optional[int] = None
    is_owner: bool = False
    type: str = 'employer'

    company: Optional['CompanySchema'] = None




