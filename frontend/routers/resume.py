from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/resumes")
templates = Jinja2Templates(directory='frontend')


@router.get("/add")
def resume_add(request: Request):
    return templates.TemplateResponse("/pages/resume/create/resume.html", {"request": request})
