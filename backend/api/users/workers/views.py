from fastapi import APIRouter, Depends

from backend.api.users.auth.token_dependencies import get_worker_by_token
from backend.api.users.workers.dependencies import update_worker_dependencies
from backend.api.users.workers.schemas import WorkerSchema

router = APIRouter(prefix='/workers', tags=['workers'])

@router.get('/me', summary='Узнать информацию о себе')
def get_my_profile(
        worker: WorkerSchema = Depends(get_worker_by_token)
):
    return worker.model_dump(exclude='password')

@router.put('/me', summary='Редактировать информацию о себе')
def update_my_profile(
        worker: WorkerSchema = Depends(update_worker_dependencies)
):
    return worker.model_dump(exclude='password')