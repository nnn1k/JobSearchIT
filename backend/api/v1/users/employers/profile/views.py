from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.utils.dependencies import get_db
from backend.core.utils.auth_utils.user_login_dependencies import get_employer_by_token
from backend.api.v1.users.employers.profile.queries import update_employer_by_id_queries
from backend.core.schemas.models.employer.employer_schema import EmployerResponseSchema
from backend.api.v1.users.employers.profile.schemas import EmployerProfileSchema
from backend.core.schemas.global_schema import DynamicSchema


router = APIRouter(prefix='/employers/me', tags=['employers'])


@router.get('', summary='Узнать информацию о себе')
async def get_my_profile(
        employer: EmployerResponseSchema = Depends(get_employer_by_token)
):
    return {
        'user': employer,
        'status': 'ok'
    }


@router.put('', summary='Редактировать информацию о себе')
async def update_my_profile(
        new_employer: EmployerProfileSchema,
        employer: EmployerResponseSchema = Depends(get_employer_by_token),
        session: AsyncSession = Depends(get_db),
):
    employer = await update_employer_by_id_queries(employer_id=employer.id, session=session, **new_employer.model_dump())
    return {
        'user': employer,
        'status': 'ok'
    }


@router.patch('', summary='Редактировать информацию о себе по одному атрибуту')
async def update_my_other(
        new_employer: DynamicSchema,
        employer: EmployerResponseSchema = Depends(get_employer_by_token),
        session: AsyncSession = Depends(get_db),
):
    employer = await update_employer_by_id_queries(employer_id=employer.id, session=session, **new_employer.model_dump())
    return {
        'user': employer,
        'status': 'ok'
    }

