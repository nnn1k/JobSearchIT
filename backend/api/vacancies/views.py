from fastapi import APIRouter, Depends

from backend.api.vacancies.dependencies import (
    create_vacancy_dependencies,
    get_vacancy_by_id_dependencies,
    delete_vacancy_by_id_dependencies,
    update_vacancy_by_id_dependencies,
)

router = APIRouter(prefix="/vacancy", tags=["vacancy"])


@router.post('/', summary='Создать вакансию')
def create_new_vacancy(
        vacancy_and_user=Depends(create_vacancy_dependencies)
):
    vacancy, user = vacancy_and_user

    if user:
        user = user.model_dump(exclude='password')
    return {
        'status': 'ok',
        'vacancy': vacancy,
        'user': user
    }


@router.get('/{vacancy_id}', summary='Посмотреть информацию о вакансии')
def get_info_on_vacancy(
        vacancy_and_user=Depends(get_vacancy_by_id_dependencies),
):
    vacancy, user, can_update = vacancy_and_user

    return {
        'status': 'ok',
        'vacancy': vacancy,
        'user': user,
        'can_update': can_update,

    }


@router.put('/{vacancy_id}', summary='Изменить вакансию')
def update_info_on_company(
        vacancy_and_user=Depends(update_vacancy_by_id_dependencies),
):
    vacancy, user = vacancy_and_user
    return {
        'vacancy': vacancy,
        'user': user,
        'status': 'ok',
    }


@router.delete('/{vacancy_id}', summary='Удалить вакансию')
def delete_info_on_company(
        vacancy_and_user=Depends(delete_vacancy_by_id_dependencies),
):
    vacancy, user = vacancy_and_user
    return {
        'user': user,
        'status': 'ok',
    }
