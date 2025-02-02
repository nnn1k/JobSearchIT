from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/employer")
templates = Jinja2Templates(directory='frontend')


@router.get("/profile")
def my_account_employer(request: Request):
    user_type = request.cookies.get("user_type")
    if user_type != "employer":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("/pages/employer/profile/profile.html", {"request": request})
