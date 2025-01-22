from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/worker")
templates = Jinja2Templates(directory='frontend')

@router.get("/profile")
def create_profile(request: Request):
    return templates.TemplateResponse("/templates/pages/profile/html_profile.html", {"request": request})
