from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from .routers import signup_router, employer_router, worker_router

templates = Jinja2Templates(directory='frontend')

router = APIRouter(include_in_schema=False)
router.include_router(signup_router)
router.include_router(employer_router)
router.include_router(worker_router)

@router.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("/templates/pages/auth/html_login.html", {"request": request})


