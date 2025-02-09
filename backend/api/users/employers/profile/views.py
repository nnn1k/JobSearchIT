from fastapi import APIRouter, Depends

from backend.api.users.employers.profile.dependencies import get_employer_by_token, put_employer_dependencies, \
    patch_employer_dependencies
from backend.api.users.employers.profile.schemas import EmployerSchema

router = APIRouter(prefix='/employers', tags=['employers'])


@router.get('/me', summary='Узнать информацию о себе')
def get_my_profile(
        employer: EmployerSchema = Depends(get_employer_by_token)
):
    return {
        'user': employer,
        'status': 'ok'
    }


@router.put('/me', summary='Редактировать информацию о себе')
def update_my_profile(
        employer: EmployerSchema = Depends(put_employer_dependencies)
):
    return {
        'user': employer,
        'status': 'ok'
    }


@router.patch('/me', summary='Редактировать информацию о себе по одному атрибуту')
def update_my_other(
        employer: EmployerSchema = Depends(patch_employer_dependencies)
):
    return {
        'user': employer,
        'status': 'ok'
    }
