from fastapi import APIRouter, Depends

from backend.api.users.workers.dependencies import put_worker_dependencies, patch_worker_dependencies, \
    get_worker_by_token
from backend.api.users.workers.schemas import WorkerSchema

router = APIRouter(prefix='/workers', tags=['workers'])

@router.get('/me', summary='Узнать информацию о себе')
def get_my_profile(
        worker: WorkerSchema = Depends(get_worker_by_token)
):
    return {'worker': worker.model_dump(exclude='password')}

@router.put('/me', summary='Редактировать информацию о себе')
def update_my_profile(
        worker: WorkerSchema = Depends(put_worker_dependencies)
):
    return {'worker': worker.model_dump(exclude='password')}

@router.patch('/me', summary='Редактировать информацию о себе по одному атрибуту')
def update_my_other(
        worker: WorkerSchema = Depends(patch_worker_dependencies)
):
    return {'worker': worker.model_dump(exclude='password')}