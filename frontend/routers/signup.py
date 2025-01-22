from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/signup")
templates = Jinja2Templates(directory='frontend')


@router.get("/worker")
def reg_worker(request: Request):
    return templates.TemplateResponse("/templates/pages/registarion/html_reg_worker.html", {"request": request})


@router.get("/employer")
def reg_employer(request: Request):
    return templates.TemplateResponse("/templates/pages/auth/html_reg_employer.html", {"request": request})


@router.get("/worker/profile")
def create_profile(request: Request):
    return templates.TemplateResponse("/templates/pages/registarion/html_step-by-step_registration.html", {"request": request})