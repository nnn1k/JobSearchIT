from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='frontend')
router = APIRouter(prefix='/vacancies')


@router.get('/add')
def add_vacancy(request: Request):
    return templates.TemplateResponse('/pages/vacancy/create/vacancy.html', {"request": request})
