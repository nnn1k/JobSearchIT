from fastapi import APIRouter, Depends

from backend.api.users.employers.dependencies import get_employer_by_token, put_employer_dependencies, patch_employer_dependencies
from backend.api.users.employers.schemas import EmployerSchema

router = APIRouter(prefix='/employers', tags=['employers'])

@router.get('/me', summary='Узнать информацию о себе')
def get_my_profile(
        employer: EmployerSchema = Depends(get_employer_by_token)
):
    return {'employer': employer.model_dump(exclude='password')}

@router.put('/me', summary='Редактировать информацию о себе')
def update_my_profile(
        employer: EmployerSchema = Depends(put_employer_dependencies)
):
    return {'worker': employer.model_dump(exclude='password')}

@router.patch('/me', summary='Редактировать информацию о себе по одному атрибуту')
def update_my_other(
        employer: EmployerSchema = Depends(patch_employer_dependencies)
):
    return {'worker': employer.model_dump(exclude='password')}