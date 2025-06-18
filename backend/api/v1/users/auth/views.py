from fastapi import APIRouter, Response, Depends, BackgroundTasks
from backend.core.schemas.user_schema import LoginSchema, RegisterSchema
from backend.core.services.auth.dependencies import get_auth_serv
from backend.core.services.auth.service import AuthService
from backend.core.utils.auth_utils.user_login_dependencies import (
    get_auth_user_by_token,
    get_worker_by_token,
    get_employer_by_token
)
from backend.core.utils.const import ACCESS_TOKEN, REFRESH_TOKEN

from backend.core.utils.other.email_utils import SendEmail

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/workers/login', summary='Вход соискателя')
async def login_worker(
        response: Response,
        login_schema: LoginSchema,
        auth_serv: AuthService = Depends(get_auth_serv)
):
    worker = await auth_serv.login_worker(login_schema=login_schema, response=response)
    return {'user': worker}


@router.post('/employers/login', summary='Вход работодателя')
async def login_employer(
        response: Response,
        login_schema: LoginSchema,
        auth_serv: AuthService = Depends(get_auth_serv)
):
    employer = await auth_serv.login_employer(login_schema=login_schema, response=response)
    return {'user': employer}


@router.post('/workers/register', summary='Регистрация соискателя')
async def register_worker(
        response: Response,
        register_schema: RegisterSchema,
        auth_serv: AuthService = Depends(get_auth_serv)
):
    worker = await auth_serv.register_worker(reg_schema=register_schema, response=response)
    return {'user': worker}


@router.post('/employers/register', summary='Регистрация работодателя')
async def register_employer(
        response: Response,
        register_schema: RegisterSchema,
        auth_serv: AuthService = Depends(get_auth_serv)
):
    employer = await auth_serv.register_employer(reg_schema=register_schema, response=response)
    return {'user': employer}


@router.get('/code', summary='Получить код')
async def get_code(
        user=Depends(get_auth_user_by_token)
):
    await SendEmail.send_code_to_email(user)
    return {
        'msg': 'Код отправлен на почту:',
        'email': user.email,
    }


@router.post('/workers/code', summary='Отправить код за соискателя')
async def send_code_worker(
        code: str,
        worker=Depends(get_worker_by_token),
        auth_serv: AuthService = Depends(get_auth_serv)
):
    new_worker = await auth_serv.confirm_worker(code=code, user=worker)
    return {'user': new_worker}


@router.post('/employers/code', summary='Отправить код за работодателя')
async def send_code_employer(
        code: str,
        employer=Depends(get_employer_by_token),
        auth_serv: AuthService = Depends(get_auth_serv)
):
    new_employer = await auth_serv.confirm_employer(code=code, user=employer)
    return {'user': new_employer}


@router.post('/logout', summary='Выход с аккаунта')
def logout_user(response: Response):
    response.delete_cookie(ACCESS_TOKEN)
    response.delete_cookie(REFRESH_TOKEN)
    response.delete_cookie('user_type')
    return {
        'status': 'ok',
        'message': 'user logged out'
    }
