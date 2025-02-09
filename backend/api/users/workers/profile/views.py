from fastapi import APIRouter, Depends

from backend.api.users.workers.profile.dependencies import (
    put_worker_dependencies,
    patch_worker_dependencies,
    get_worker_by_token
)
from backend.api.users.workers.profile.schemas import WorkerSchema

router = APIRouter(prefix='/me', tags=['workers_profile'])

@router.get('/', summary='Узнать информацию о себе')
def get_my_profile(
        worker: WorkerSchema = Depends(get_worker_by_token)
):
    return {
        'user': worker,
        'status': 'ok'
    }


@router.put('/', summary='Редактировать информацию о себе')
def update_my_profile(
        worker: WorkerSchema = Depends(put_worker_dependencies)
):
    return {
        'user': worker,
        'status': 'ok'
    }


@router.patch('/', summary='Редактировать информацию о себе по одному атрибуту')
def update_my_other(
        worker: WorkerSchema = Depends(patch_worker_dependencies)
):
    return {
        'user': worker,
        'status': 'ok'
    }
