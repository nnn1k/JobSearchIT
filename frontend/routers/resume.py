from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/resume")
templates = Jinja2Templates(directory='frontend')

@router.get("/add")
def resume_add(request: Request):
    return templates.TemplateResponse("/pages/resume/resume.html", {"request": request})
