from backend.api.users.employers.profile.dependencies import get_employer_by_token
from backend.api.users.workers.profile.dependencies import get_worker_by_token
from backend.utils.auth_utils.token_dependencies import ACCESS_TOKEN, REFRESH_TOKEN
from fastapi import APIRouter, Cookie, Response, HTTPException, status

from backend.api.users.auth.schemas import LoginSchema, RegisterSchema, UserType
from backend.api.users.employers.profile.repository import get_employer_repo
from backend.api.users.workers.profile.repository import get_worker_repo
from backend.schemas.global_schema import CodeSchema
from backend.api.users.auth.dependencies import (
    check_user_code_dependencies,
    create_token, login_user, register_user,
)

from backend.utils.other.email_func import SendEmail

router = APIRouter(prefix="/auth", tags=["auth"])
type_router = APIRouter(prefix="/{user_type}")


@type_router.post('/login', summary='Вход пользователя')
async def login_user_views(
        response: Response,
        user_type: UserType,
        schema: LoginSchema,
):
    match user_type:
        case UserType.employer:
            repo = get_employer_repo()
        case UserType.worker:
            repo = get_worker_repo()
        case _:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = await login_user(schema, repo)
    return create_token(response, user)


@type_router.post('/register', summary='Регистрация пользователя')
async def register_user_views(
        response: Response,
        user_type: UserType,
        schema: RegisterSchema,
):
    match user_type:
        case UserType.employer:
            repo = get_employer_repo()
        case UserType.worker:
            repo = get_worker_repo()
        case _:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = await register_user(schema, repo)
    return create_token(response, user)


@type_router.get('/code', summary='Отправка кода')
async def get_code(
        user_type: UserType,
        access_token=Cookie(None)
):
    match user_type:
        case UserType.employer:
            user = await get_employer_by_token(access_token)
        case UserType.worker:
            user = await get_worker_by_token(access_token)
        case _:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    await SendEmail.send_code_to_email(user, user.type)
    return {
        'message': 'Код отправлен на почту:',
        'email': user.email,
        'status': 'ok'
    }


@type_router.post('/code', summary='Проверка кода')
async def send_code(
        user_type: UserType,
        code: CodeSchema,
        access_token=Cookie(None)
):
    match user_type:
        case UserType.employer:
            user = await get_employer_by_token(access_token)
            repo = get_employer_repo()
        case UserType.worker:
            user = await get_worker_by_token(access_token)
            repo = get_worker_repo()
        case _:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await check_user_code_dependencies(user, repo, code)
    return {
        'user': user,
        'status': 'ok',
    }


@router.post('/logout', summary='Выход с аккаунта')
def logout_user(response: Response):
    response.delete_cookie(ACCESS_TOKEN)
    response.delete_cookie(REFRESH_TOKEN)
    response.delete_cookie('user_type')
    return {
        'status': 'ok',
        'message': 'user logged out'
    }


router.include_router(type_router)
