from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/employer")
templates = Jinja2Templates(directory='frontend')


@router.get("/profile")
def my_account_employer(request: Request):
    return templates.TemplateResponse("/pages/employer/profile/profile.html", {"request": request})
