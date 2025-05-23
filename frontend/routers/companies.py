from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory='frontend')

router = APIRouter(prefix='/companies', include_in_schema=False)


@router.get('/add')
def add_company(request: Request):
    user_type = request.cookies.get("user_type")
    if user_type != "employer":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse('/pages/company/create/create.html', {"request": request, 'user_type': user_type})


@router.get('/{company_id}')
def get_company(request: Request):
    user_type = request.cookies.get("user_type")
    return templates.TemplateResponse('/pages/company/company.html', {"request": request, 'user_type': user_type})



