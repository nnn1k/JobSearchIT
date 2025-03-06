from fastapi.responses import RedirectResponse

from .signup import router as signup_router
from .employer import router as employer_router
from .worker import router as worker_router
from .companies import router as company_router
from .vacancies import router as vacancy_router
from .resume import router as resume_router
from .feedbacks import router as feedback_router


from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='frontend')

router = APIRouter(include_in_schema=False)
router.include_router(signup_router)
router.include_router(employer_router)
router.include_router(worker_router)
router.include_router(company_router)
router.include_router(vacancy_router)
router.include_router(resume_router)
router.include_router(feedback_router)


@router.get("/")
def home_page_worker(request: Request):
    user_type = request.cookies.get("user_type")
    if user_type == "worker":
        return RedirectResponse(url="/vacancies/?page=1")
    if user_type == "employer":
        return RedirectResponse(url="/employer")
    return templates.TemplateResponse("/pages/start_by_worker/start_page_for_worker.html", {"request": request})


@router.get("/employer")
def home_page_employer(request: Request):
    user_type = request.cookies.get("user_type")
    if user_type == "employer":
        return RedirectResponse(url="/resumes/?page=1")
    if user_type == "worker":
        return RedirectResponse(url="/")
    return templates.TemplateResponse("/pages/start_for_employer/start_page.html", {"request": request})


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("/pages/auth/login/login.html", {"request": request})




