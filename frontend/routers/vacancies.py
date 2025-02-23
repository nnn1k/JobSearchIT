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
def get_vacancy(request: Request):
    user_type = request.cookies.get("user_type")
    return templates.TemplateResponse('/pages/vacancy/one/vacancy.html', {"request": request, 'user_type': user_type})


@router.get('/{vacancy_id}/edit')
def get_vacancy(request: Request):
    user_type = request.cookies.get("user_type")
    if user_type != "employer":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse('/pages/vacancy/edit/vacancy.html', {"request": request})


@router.get('/{vacancy_id}/edit/skills')
def get_vacancy_skills_for_edit(request: Request):
    user_type = request.cookies.get("user_type")
    if user_type != "employer":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse('/pages/vacancy/edit/edit_skills/vacancy.html', {"request": request})