from fastapi import APIRouter, Depends

from backend.utils.auth_utils.user_login_dependencies import get_employer_by_token
from backend.api.users.employers.profile.queries import update_employer_by_id_queries
from backend.schemas.employer_schema import EmployerResponseSchema
from backend.api.users.employers.profile.schemas import EmployerProfileSchema
from backend.schemas.global_schema import DynamicSchema

router = APIRouter(prefix='/employers', tags=['employers'])


@router.get('/me', summary='Узнать информацию о себе')
async def get_my_profile(
        employer: EmployerResponseSchema = Depends(get_employer_by_token)
):
    return {
        'user': employer,
        'status': 'ok'
    }


@router.put('/me', summary='Редактировать информацию о себе')
async def update_my_profile(
        new_employer: EmployerProfileSchema,
        employer: EmployerResponseSchema = Depends(get_employer_by_token)
):
    employer = await update_employer_by_id_queries(employer_id=employer.id, **new_employer.model_dump())
    return {
        'user': employer,
        'status': 'ok'
    }


@router.patch('/me', summary='Редактировать информацию о себе по одному атрибуту')
async def update_my_other(
        new_employer: DynamicSchema,
        employer: EmployerResponseSchema = Depends(get_employer_by_token)
):
    employer = await update_employer_by_id_queries(employer_id=employer.id, **new_employer.model_dump())
    return {
        'user': employer,
        'status': 'ok'
    }
