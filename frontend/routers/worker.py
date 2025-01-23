from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/worker")
templates = Jinja2Templates(directory='frontend')

@router.get("/profile")
def my_account(request: Request):
    return templates.TemplateResponse("/pages/worker/profile/profile.html", {"request": request})
