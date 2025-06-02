from fastapi import APIRouter, Depends

from backend.core.schemas.models.worker.worker_schema import WorkerProfileSchema
from backend.core.schemas.global_schema import DynamicSchema
from backend.core.services.users.dependencies import get_user_serv
from backend.core.services.users.service import UserService
from backend.core.utils.auth_utils.user_login_dependencies import get_worker_by_token

from backend.core.schemas import WorkerSchemaRel, WorkerSchema

router = APIRouter(prefix='/me', tags=['workers'])


@router.get('', summary='Узнать информацию о себе')
async def get_my_profile(
        worker: WorkerSchemaRel = Depends(get_worker_by_token),
        user_serv: UserService = Depends(get_user_serv)
):
    new_worker = await user_serv.get_worker_rel(id=worker.id)
    return {
        'user': new_worker,
    }


@router.put('', summary='Редактировать информацию о себе')
async def update_my_profile(
        new_worker: WorkerProfileSchema,
        worker: WorkerSchema = Depends(get_worker_by_token),
        user_serv: UserService = Depends(get_user_serv)
):
    new_worker = await user_serv.update_worker(worker_id=worker.id, **new_worker.model_dump())
    return {
        'user': new_worker,
    }


@router.patch('', summary='Редактировать информацию о себе по одному атрибуту')
async def update_my_other(
        new_worker: DynamicSchema,
        worker: WorkerSchema = Depends(get_worker_by_token),
        user_serv: UserService = Depends(get_user_serv)
):
    new_worker = await user_serv.update_worker(worker_id=worker.id, **new_worker.model_dump())
    return {
        'user': new_worker,
    }
