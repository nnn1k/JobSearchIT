from fastapi import Depends

from backend.api.users.employers.dependencies import get_employer_by_token
from backend.api.users.employers.schemas import EmployerSchema


async def create_company_dependencies(
        owner: EmployerSchema = Depends(get_employer_by_token)
):
    pass