from backend.api.companies.schemas import CompanySchema
from backend.api.users.employers.schemas import EmployerSchema
from backend.api.users.workers.schemas import WorkerSchema
from backend.schemas.global_schema import GlobalSchema


def check_can_update(user: WorkerSchema | EmployerSchema, obj: GlobalSchema) -> bool:
    if not isinstance(user, EmployerSchema):
        return False
    if isinstance(obj, CompanySchema):
        return user.company_id == obj.id
    elif hasattr(obj, 'company_id'):
        return user.company_id == obj.company_id
    return False
