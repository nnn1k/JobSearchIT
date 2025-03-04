from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.users.workers.profile.queries import update_worker_by_id_queries
from backend.api.users.workers.profile.schemas import WorkerProfileSchema
from backend.database.utils.dependencies import get_db
from backend.schemas.global_schema import DynamicSchema
from backend.utils.auth_utils.user_login_dependencies import get_worker_by_token

from backend.schemas import WorkerResponseSchema

router = APIRouter(prefix='/me', tags=['workers'])


@router.get('', summary='Узнать информацию о себе')
async def get_my_profile(
        worker: WorkerResponseSchema = Depends(get_worker_by_token)
):
    return {
        'user': worker,
        'status': 'ok'
    }


@router.put('', summary='Редактировать информацию о себе')
async def update_my_profile(
        new_worker: WorkerProfileSchema,
        worker: WorkerResponseSchema = Depends(get_worker_by_token),
        session: AsyncSession = Depends(get_db),
):
    worker = await update_worker_by_id_queries(worker_id=worker.id, session=session, **new_worker.model_dump())
    return {
        'user': worker,
        'status': 'ok'
    }


@router.patch('', summary='Редактировать информацию о себе по одному атрибуту')
async def update_my_other(
        new_worker: DynamicSchema,
        worker: WorkerResponseSchema = Depends(get_worker_by_token),
        session: AsyncSession = Depends(get_db),
):
    worker = await update_worker_by_id_queries(worker_id=worker.id, session=session, **new_worker.model_dump())
    return {
        'user': worker,
        'status': 'ok'
    }
