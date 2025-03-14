from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory='frontend')
router = APIRouter(prefix='/chats')


@router.get('/')
def chats_all(request: Request):
    user_type = request.cookies.get("user_type")
    if not user_type:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("/pages/chats/chats.html", {"request": request, 'user_type': user_type})
