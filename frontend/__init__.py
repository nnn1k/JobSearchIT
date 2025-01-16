from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="frontend")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("/templates/pages/auth/html_login.html", {"request": request})



