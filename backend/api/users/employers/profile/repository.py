from backend.database.utils.repository import AlchemyRepository
from backend.api.users.employers.profile.schemas import EmployerSchema, EmployerResponseSchema
from backend.database.models.employer.Employer import EmployersOrm
from backend.utils.auth_utils.check_func import exclude_password


class EmployerRepository(AlchemyRepository):
    db_model = EmployersOrm
    schema = EmployerSchema
    response_schema = EmployerResponseSchema
    user_type = 'employer'


def get_employer_repo() -> EmployerRepository:
    return EmployerRepository()


async def get_employer_by_id(id: int) -> EmployerResponseSchema:
    employer_repo = get_employer_repo()
    employer = await employer_repo.get_one(id=id)
    return exclude_password(employer, EmployerResponseSchema)
