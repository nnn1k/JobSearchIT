from fastapi import APIRouter, Depends

router = APIRouter(prefix="/vacancies", tags=["vacancies"])

'''
вытащить пользователя из cookie: user = Depends(get_user_by_token) api/users/auth/token_dependencies
для работы с бд у каждой сущности если repository.py где по функции vacancy_repo = get_vacancy_repo() будет возвращатся объект этого репозитория
у которого есть 5 функций get_one, get_all, add_one, update_one, delete_one, куда передаются атрибуты к примеру:
vacancy_repo.get_one(id=..., name=...) любой атрибут
'''