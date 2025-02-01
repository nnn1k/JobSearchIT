from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='frontend')
router = APIRouter(prefix='/vacancies')


@router.get('/123123')
def add_vacancy(request: Request):
    user_type = request.cookies.get("user_type")
    return templates.TemplateResponse('/pages/vacancy/vacancy.html', {"request": request, 'user_type': user_type})


@router.get('/add')
def add_vacancy(request: Request):
    return templates.TemplateResponse('/pages/vacancy/create/vacancy.html', {"request": request})


