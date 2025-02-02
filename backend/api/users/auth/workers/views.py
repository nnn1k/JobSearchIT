from fastapi import APIRouter, Depends, Response
from starlette.responses import RedirectResponse

from backend.utils.auth_utils.AuthJWT import jwt_token, Token
from backend.utils.auth_utils.auth_dependencies import confirm_email_response, send_code_response
from backend.utils.auth_utils.token_dependencies import ACCESS_TOKEN, REFRESH_TOKEN
from backend.api.users.auth.workers.dependencies import (
    register_worker_dependencies,
    login_worker_dependencies,
    check_code_dependencies,
    get_code_dependencies,
)
from backend.api.users.workers.profile.schemas import WorkerResponseSchema

router = APIRouter(prefix='/workers', tags=['workers_auth'])


@router.post('/login', summary='Вход работника')
async def login(
        response: Response,
        worker: WorkerResponseSchema = Depends(login_worker_dependencies),
):
    access_token = jwt_token.create_access_token(id=worker.id, user_type=worker.type)
    refresh_token = jwt_token.create_refresh_token(id=worker.id, user_type=worker.type)

    response.set_cookie(ACCESS_TOKEN, access_token)
    response.set_cookie(REFRESH_TOKEN, refresh_token)
    response.set_cookie('user_type', worker.type)
    token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    return {
        'user': worker,
        'token': token,
        'status': 'ok'
    }


@router.post('/register', summary='Регистрация работника')
async def register(
        worker: WorkerResponseSchema = Depends(register_worker_dependencies)
):
    return RedirectResponse(url='/api/auth/workers/login')


@router.get('/code', summary='Отправить код на почту')
async def get_code(
        worker: WorkerResponseSchema = Depends(get_code_dependencies)
):
    return send_code_response(worker.email)


@router.post('/code', summary='Проверка кода')
async def send_code(
        worker: WorkerResponseSchema = Depends(check_code_dependencies)
):
    return confirm_email_response(worker.email)
