from pydantic import BaseModel

from backend.api.users.employers.schemas import EmployerSchema, EmployerResponseSchema
from backend.api.users.workers.schemas import WorkerSchema, WorkerResponseSchema
from backend.schemas.global_schema import GlobalSchema


def check_employer_can_update(user, obj: GlobalSchema) -> bool:
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

def check_worker_can_update(user: WorkerSchema | EmployerSchema, obj: GlobalSchema) -> bool:
    if not isinstance(user, WorkerResponseSchema):
        return False
    if hasattr(obj, 'worker_id'):
        return user.id == obj.worker_id
    return False

def exclude_password(user: BaseModel, response_schema: BaseModel):
    user_response = user.model_dump(exclude='password')
    return response_schema.model_validate(user_response, from_attributes=True)
