from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='frontend/templates')


router = APIRouter(include_in_schema=False)

@router.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("/pages/auth/html_login.html", {"request": request})

@router.get("/signup/worker")
def reg_worker(request: Request):
    return templates.TemplateResponse("/pages/auth/html_reg_worker.html", {"request": request})


@router.get("/signup/employer")
def reg_employer(request: Request):
    return templates.TemplateResponse("/pages/auth/html_reg_employer.html", {"request": request})



