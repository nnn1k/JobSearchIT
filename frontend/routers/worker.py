from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/worker")
templates = Jinja2Templates(directory='frontend')


@router.get("/profile")
def my_account_worker(request: Request):
    user_type = request.cookies.get("user_type")
    if user_type != "worker":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("/pages/worker/profile/profile.html", {"request": request})
