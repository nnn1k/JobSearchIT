from typing import Optional

from backend.database.utils.repository import AlchemyRepository
from backend.api.users.employers.schemas import EmployerSchema, EmployerResponseSchema
from backend.database.models.employer import EmployersOrm


class EmployerRepository(AlchemyRepository):
    db_model = EmployersOrm
    schema = EmployerSchema
    user_type = 'employer'

def get_employer_repo() -> EmployerRepository:
    return EmployerRepository()

async def get_employer_by_id(id: int) -> EmployerResponseSchema:
    employer_repo = get_employer_repo()
    employer = await employer_repo.get_one(id=id)
    employer_response = employer.model_dump(exclude='password')
    return EmployerResponseSchema.model_validate(employer_response, from_attributes=True)
