from fastapi import Depends, APIRouter

router = APIRouter(prefix='/companies')

@router.get('/', summary='Создать компанию')
def create_new_company(

):
    pass
