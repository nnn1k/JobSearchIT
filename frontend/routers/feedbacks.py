from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory='frontend')
router = APIRouter(prefix='/feedbacks')


@router.get('/')
def feedbacks_all(request: Request):
    user_type = request.cookies.get("user_type")
    return templates.TemplateResponse("/pages/feedbacks/feedbacks.html", {"request": request, 'user_type': user_type})

