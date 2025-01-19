from fastapi import APIRouter, Response, Depends
from fastapi.responses import RedirectResponse

from backend.api.users.auth.AuthJWT import jwt_token, Token
from backend.api.users.auth.employers.dependencies import login_employer_dependencies, register_employer_dependencies, \
    get_code_dependencies, check_code_dependencies
from backend.api.users.auth.token_dependencies import ACCESS_TOKEN, REFRESH_TOKEN
from backend.api.users.employers.schemas import EmployerSchema

router = APIRouter(prefix="/employers", tags=["auth_employers"])

@router.post('/login', summary='Вход работодателя')
async def login(
        response: Response,
        employer: EmployerSchema = Depends(login_employer_dependencies),
):
    access_token = jwt_token.create_access_token(id=employer.id, user_type='employer')
    refresh_token = jwt_token.create_refresh_token(id=employer.id, user_type='employer')

    response.set_cookie(ACCESS_TOKEN, access_token)
    response.set_cookie(REFRESH_TOKEN, refresh_token)
    token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    return {
        'employer': employer.model_dump(exclude='password'),
        'token': token
    }

@router.post('/register', summary='Регистрация работника')
async def register(
        worker: EmployerSchema = Depends(register_employer_dependencies)
):
    return RedirectResponse(url='/api/auth/employers/login')

@router.get('/code', summary='Отправить код на почту')
async def get_code(
        employer: EmployerSchema = Depends(get_code_dependencies)
):
    return {
        'message': 'Код отправлен на почту:',
        'email': employer.email
    }

@router.post('/code', summary='Проверка кода')
async def send_code(
        employer: EmployerSchema = Depends(check_code_dependencies)
):
    return {
        'message': 'Почта подтверждена',
        'email': employer.email
    }