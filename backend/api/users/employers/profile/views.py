from fastapi import APIRouter, Depends

from backend.utils.auth_utils.user_login_dependencies import get_employer_by_token
from backend.api.users.employers.profile.queries import update_employer_by_id_queries
from backend.schemas.models.employer.employer_schema import EmployerResponseSchema
from backend.api.users.employers.profile.schemas import EmployerProfileSchema
from backend.schemas.global_schema import DynamicSchema
from backend.utils.other.time_utils import time_it_async

router = APIRouter(prefix='/employers/me', tags=['employers'])


@router.get('', summary='Узнать информацию о себе')
@time_it_async
async def get_my_profile(
        employer: EmployerResponseSchema = Depends(get_employer_by_token)
):
    return {
        'user': employer,
        'status': 'ok'
    }


@router.put('', summary='Редактировать информацию о себе')
@time_it_async
async def update_my_profile(
        new_employer: EmployerProfileSchema,
        employer: EmployerResponseSchema = Depends(get_employer_by_token)
):
    employer = await update_employer_by_id_queries(employer_id=employer.id, **new_employer.model_dump())
    return {
        'user': employer,
        'status': 'ok'
    }


@router.patch('', summary='Редактировать информацию о себе по одному атрибуту')
@time_it_async
async def update_my_other(
        new_employer: DynamicSchema,
        employer: EmployerResponseSchema = Depends(get_employer_by_token)
):
    employer = await update_employer_by_id_queries(employer_id=employer.id, **new_employer.model_dump())
    return {
        'user': employer,
        'status': 'ok'
    }

