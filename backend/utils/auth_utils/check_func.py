from typing import Any
from backend.api.users.employers.profile.schemas import EmployerResponseSchema
from backend.api.users.workers.profile.schemas import WorkerResponseSchema
from backend.utils.other.type_utils import BaseVar, UserVar


def check_employer_can_update(user, obj: BaseVar) -> bool:
    from backend.api.companies.schemas import CompanySchema
    if not isinstance(user, EmployerResponseSchema):
        return False
    if not user.is_owner:
        return False
    if isinstance(obj, CompanySchema):
        return user.company_id == obj.id
    elif hasattr(obj, 'company_id'):
        return user.company_id == obj.company_id
    return False

def check_worker_can_update(user: UserVar, obj: BaseVar) -> bool:
    if not isinstance(user, WorkerResponseSchema):
        return False
    if hasattr(obj, 'worker_id'):
        return user.id == obj.worker_id
    return False

def exclude_password(user: UserVar, response_schema: BaseVar):
    user_response = user.model_dump(exclude={'password'})
    return response_schema.model_validate(user_response, from_attributes=True)
