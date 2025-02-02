from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory='frontend')
router = APIRouter(prefix='/vacancies')



@router.get('/add')
def add_vacancy(request: Request):
    user_type = request.cookies.get("user_type")
    if user_type != "employer":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse('/pages/vacancy/create/vacancy.html', {"request": request})


@router.get('/{vacancy_id}')
def add_vacancy(request: Request):
    user_type = request.cookies.get("user_type")
    return templates.TemplateResponse('/pages/vacancy/vacancy.html', {"request": request, 'user_type': user_type})