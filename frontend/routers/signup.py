from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/signup")
templates = Jinja2Templates(directory='frontend')


@router.get("/worker")
def signup_worker(request: Request):
    return templates.TemplateResponse("/pages/auth/signup/worker/signup/worker.html", {"request": request})


@router.get("/employer")
def signup_employer(request: Request):
    return templates.TemplateResponse("/pages/auth/signup/employer/signup/employer.html", {"request": request})


@router.get("/worker/profile")
def create_profile_worker(request: Request):
    user_type = request.cookies.get("user_type")
    if user_type != "worker":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("/pages/auth/signup/worker/step_by_step/worker.html", {"request": request})


@router.get("/employer/profile")
def create_profile_employer(request: Request):
    user_type = request.cookies.get("user_type")
    if user_type != "employer":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("/pages/auth/signup/employer/step_by_step/employer.html", {"request": request})
