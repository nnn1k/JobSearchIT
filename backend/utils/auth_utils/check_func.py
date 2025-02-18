from backend.schemas import EmployerResponseSchema
from backend.schemas import WorkerResponseSchema
from backend.utils.other.type_utils import BaseVar, UserVar
from backend.utils.other.logger_utils import logger


def check_employer_can_update(user, obj: BaseVar) -> bool:
    from backend.schemas import CompanySchema
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


