from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/employer")
templates = Jinja2Templates(directory='frontend')


@router.get("/profile")
def my_account(request: Request):
    return templates.TemplateResponse("/templates/pages/profile_employer/profile_employer.html", {"request": request})