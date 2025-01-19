from fastapi import APIRouter, Depends

from backend.api.users.auth.token_dependencies import get_employer_by_token
from backend.api.users.employers.schemas import EmployerSchema

router = APIRouter(prefix='/employers', tags=['employers'])

@router.get('/me', summary='Узнать информацию о себе')
def get_my_profile(
        employer: EmployerSchema = Depends(get_employer_by_token)
):
    return {'employer': employer.model_dump(exclude='password')}
