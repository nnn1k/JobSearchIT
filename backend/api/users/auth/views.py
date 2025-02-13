from backend.api.users.auth.queries import login_user_queries, register_user_queries, update_code_queries
from backend.utils.auth_utils.user_login_dependencies import get_employer_by_token, get_user_by_token, \
    get_worker_by_token
from backend.utils.auth_utils.token_dependencies import ACCESS_TOKEN, REFRESH_TOKEN
from fastapi import APIRouter, Cookie, Depends, Response, HTTPException, status

from backend.api.users.auth.schemas import CodeSchema, LoginSchema, RegisterSchema, UserType
from backend.api.users.auth.dependencies import (
    create_token,
    get_login_db_model,
)

from backend.utils.other.email_func import SendEmail
from backend.utils.other.redis_func import get_code_from_redis

router = APIRouter(prefix="/auth", tags=["auth"])
type_router = APIRouter(prefix="/{user_type}")


@type_router.post('/login', summary='Вход пользователя')
async def login_user_views(
        response: Response,
        user_type: UserType,
        schema: LoginSchema,
):
    db_model, response_schema = get_login_db_model(user_type)
    user = await login_user_queries(schema, db_model, response_schema)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )
    return create_token(response, user)


@type_router.post('/register', summary='Регистрация пользователя')
async def register_user_views(
        response: Response,
        user_type: UserType,
        schema: RegisterSchema,
):
    db_model, response_schema = get_login_db_model(user_type)
    if schema.password != schema.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="password mismatch",
        )
    new_user = await register_user_queries(schema, db_model, response_schema)
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user is exist",
        )
    return create_token(response, schema)


@type_router.get('/code', summary='Отправка кода')
async def get_code(
        user_type: UserType,
        access_token=Cookie(None),
        refresh_token=Cookie(None),
):
    match user_type:
        case UserType.employer:
            user = await get_employer_by_token(access_token, refresh_token)
        case UserType.worker:
            user = await get_worker_by_token(access_token, refresh_token)
        case _:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    await SendEmail.send_code_to_email(user, user_type.value)
    return {
        'message': 'Код отправлен на почту:',
        'email': user.email,
        'status': 'ok'
    }


@type_router.post('/code', summary='Проверка кода')
async def send_code(
        user_type: UserType,
        code: CodeSchema,
        user=Depends(get_user_by_token)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    db_model, response_schema = get_login_db_model(user_type)
    new_code = await get_code_from_redis(user_type.value, user.id)
    if code.code != new_code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect code",
        )
    user = await update_code_queries(user.id, db_model, response_schema)

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
