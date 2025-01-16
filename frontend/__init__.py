from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='frontend/templates')


router = APIRouter(include_in_schema=False)

@router.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("/pages/auth/html_login.html", {"request": request})



