from .signup import router as signup_router
from .employer import router as employer_router
from .worker import router as worker_router

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='frontend')

router = APIRouter(include_in_schema=False)
router.include_router(signup_router)
router.include_router(employer_router)
router.include_router(worker_router)

@router.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("/pages/auth/login/login.html", {"request": request})
