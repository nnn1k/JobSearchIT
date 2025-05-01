from fastapi import APIRouter, Depends

from backend.core.schemas.models.employer.employer_schema import EmployerSchema
from backend.core.services.users.dependencies import get_user_serv
from backend.core.services.users.service import UserService
from backend.core.utils.auth_utils.user_login_dependencies import get_employer_by_token
from backend.api.v1.users.employers.profile.schemas import EmployerProfileSchema
from backend.core.schemas.global_schema import DynamicSchema

router = APIRouter(prefix='/employers/me', tags=['employers'])


@router.get('', summary='Узнать информацию о себе')
async def get_my_profile(
        employer: EmployerSchema = Depends(get_employer_by_token),
        user_serv: UserService = Depends(get_user_serv)
):
    new_employer = await user_serv.get_employer_rel(id=employer.id)
    return {
        'user': new_employer,
    }


@router.put('', summary='Редактировать информацию о себе')
async def update_my_profile(
        new_employer: EmployerProfileSchema,
        employer: EmployerSchema = Depends(get_employer_by_token),
        user_serv: UserService = Depends(get_user_serv)
):
    new_employer = await user_serv.update_employer(employer_id=employer.id, **new_employer.model_dump())
    return {
        'user': new_employer,
    }


@router.patch('', summary='Редактировать информацию о себе по одному атрибуту')
async def update_my_other(
        new_employer: DynamicSchema,
        employer: EmployerSchema = Depends(get_employer_by_token),
        user_serv: UserService = Depends(get_user_serv),
):
    new_employer = await user_serv.update_employer(employer_id=employer.id, **new_employer.model_dump())
    return {
        'user': new_employer,
    }
