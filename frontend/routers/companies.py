from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='frontend')

router = APIRouter(prefix='/companies', include_in_schema=False)


@router.get('/add')
def add_company(request: Request):
    return templates.TemplateResponse('/pages/company/create/create.html', {"request": request})


@router.get('/{company_id}')
def get_company(request: Request):
    return templates.TemplateResponse('/pages/company/company.html', {"request": request})



