from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/employer")
templates = Jinja2Templates(directory='frontend')
