from fastapi import APIRouter, Depends, Response
from starlette.responses import RedirectResponse

from backend.api.users.auth.AuthJWT import jwt_token, Token
from backend.api.users.auth.token_dependencies import ACCESS_TOKEN, REFRESH_TOKEN
from backend.api.users.auth.workers.dependencies import (
    register_worker_dependencies,
    login_worker_dependencies,
    check_code_dependencies,
    get_code_dependencies, refresh_token_dependencies
)
from backend.api.users.workers.schemas import WorkerSchema


router = APIRouter(prefix='/workers', tags=['auth_workers'])


@router.post('/login', summary='Вход работника')
async def login(
        response: Response,
        worker: WorkerSchema = Depends(login_worker_dependencies),
):
    access_token = jwt_token.create_access_token(id=worker.id)
    refresh_token = jwt_token.create_refresh_token(id=worker.id)

    response.set_cookie(ACCESS_TOKEN, access_token)
    response.set_cookie(REFRESH_TOKEN, refresh_token)
    token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    return {
        'worker': worker.model_dump(exclude='password'),
        'token': token
    }

@router.post('/register', summary='Регистрация работника')
async def register(
        worker: WorkerSchema = Depends(register_worker_dependencies)
):
    return RedirectResponse(url='/api/auth/workers/login')


@router.get('/code', summary='Отправить код на почту')
async def get_code(
        worker: WorkerSchema = Depends(get_code_dependencies)
):
    return {
        'message': 'Код отправлен на почту:',
        'email': worker.email
    }

@router.post('/code', summary='Проверка кода')
async def send_code(
        worker: WorkerSchema = Depends(check_code_dependencies)
):
    return {
        'message': 'Почта подтверждена',
        'email': worker.email
    }

@router.post('/refresh_token')
async def refresh_token():
    Depends(refresh_token_dependencies)
    return {'refresh': True}



