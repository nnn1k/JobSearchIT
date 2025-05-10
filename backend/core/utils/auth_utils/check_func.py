from backend.core.schemas.models.employer.employer_schema import EmployerSchema
from backend.core.schemas import EmployerSchemaRel, WorkerSchema
from backend.core.schemas import WorkerSchemaRel
from backend.core.utils.other.type_utils import BaseVar, UserVar


def check_employer_can_update(user, obj: BaseVar) -> bool:
    from backend.core.schemas import CompanySchema
    if not hasattr(user, 'company_id'):
        return False
    if not user.is_owner:
        return False
    if isinstance(obj, CompanySchema):
        return user.company_id == obj.id
    elif hasattr(obj, 'company_id'):
        return user.company_id == obj.company_id
    return False


def check_worker_can_update(user: UserVar, obj: BaseVar) -> bool:
    if not isinstance(user, WorkerSchema):
        return False
    if hasattr(obj, 'worker_id'):
        return user.id == obj.worker_id
    return False


