from backend.database.utils.repository import AlchemyRepository
from backend.api.users.employers.schemas import EmployerSchema
from backend.database.models.employer import EmployersOrm


class EmployerRepository(AlchemyRepository):
    db_model = EmployersOrm
    schema = EmployerSchema
    user_type = 'employer'

def get_employer_repo():
    return EmployerRepository()
