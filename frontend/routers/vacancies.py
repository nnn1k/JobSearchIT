from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='frontend')

router = APIRouter(prefix='/vacancy', include_in_schema=False)



