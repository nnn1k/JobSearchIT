from fastapi import APIRouter, Depends

from backend.api.vacancies.dependencies import (create_vacancy_dependencies, get_vacancy_by_id_dependencies,
                                                delete_vacancy_by_id_dependencies)
from backend.api.vacancies.schemas import VacancySchema
from backend.api.users.employers.schemas import EmployerSchema

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.post('/', summary='Создать вакансию')
def create_new_vacancy(
    owner_and_vacancy=Depends(create_vacancy_dependencies)
):
    vacancy, owner = owner_and_vacancy

    if owner:
        owner = owner.model_dump(exclude='password')
    return {
        'status': 'ok',
        'vacancy': vacancy,
        'owner': owner
    }


@router.get('/{vacancy_id}', summary='Посмотреть информацию о вакансии')
def get_info_on_vacancy(
        vacancy_and_user=Depends(get_vacancy_by_id_dependencies),
):
    vacancy, user, can_update = vacancy_and_user
    if user:
        user = user.model_dump(exclude='password')
    return {
        'status': 'ok',
        'vacancy': vacancy,
        'user': user,
        'can_update': can_update
    }


@router.delete('/{vacancy_id}', summary='Удалить вакансию')
def delete_info_on_company(
        vacancy_and_user=Depends(delete_vacancy_by_id_dependencies),
):
    user = vacancy_and_user
    if user:
        user = user.model_dump(exclude='password')
    return {
        'user_who_deleted': user,
        'status': 'ok',
        'message': 'Vacancy was remove'
    }