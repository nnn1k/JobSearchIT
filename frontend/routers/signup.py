from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/signup")
templates = Jinja2Templates(directory='frontend')


@router.get("/worker")
def signup_worker(request: Request):
    return templates.TemplateResponse("/templates/pages/signup_worker/signup_worker.html", {"request": request})


@router.get("/employer")
def signup_employer(request: Request):
    return templates.TemplateResponse("/templates/pages/signup_employer/signup_employer.html", {"request": request})


@router.get("/worker/profile")
def create_profile_worker(request: Request):
    return templates.TemplateResponse("/templates/pages/signup_worker/step-by-step_signup_worker.html", {"request": request})


@router.get("/employer/profile")
def create_profile_worker(request: Request):
    return templates.TemplateResponse("/templates/pages/signup_employer/step-by-step_signup_employer.html", {"request": request})