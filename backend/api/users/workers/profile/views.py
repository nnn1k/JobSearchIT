from fastapi import APIRouter, Depends

from backend.api.users.workers.profile.dependencies import (
    put_worker_dependencies,
    patch_worker_dependencies,
    get_worker_by_token
)

from backend.schemas import WorkerResponseSchema

router = APIRouter(prefix='/me', tags=['workers_profile'])

@router.get('/', summary='Узнать информацию о себе')
def get_my_profile(
        worker: WorkerResponseSchema = Depends(get_worker_by_token)
):
    return {
        'user': worker,
        'status': 'ok'
    }


@router.put('/', summary='Редактировать информацию о себе')
def update_my_profile(
        worker: WorkerResponseSchema = Depends(put_worker_dependencies)
):
    return {
        'user': worker,
        'status': 'ok'
    }


@router.patch('/', summary='Редактировать информацию о себе по одному атрибуту')
def update_my_other(
        worker: WorkerResponseSchema = Depends(patch_worker_dependencies)
):
    return {
        'user': worker,
        'status': 'ok'
    }
