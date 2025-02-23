from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/resumes")
templates = Jinja2Templates(directory='frontend')


@router.get('/add')
def resume_add(request: Request):
    user_type = request.cookies.get("user_type")
    if user_type != "worker":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("/pages/resume/create/resume.html", {"request": request, 'user_type': user_type})


@router.get('/{resume_id}')
def resume_get(request: Request):
    user_type = request.cookies.get("user_type")
    return templates.TemplateResponse("/pages/resume/one/resume.html", {"request": request, 'user_type': user_type})






