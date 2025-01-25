from fastapi import Depends, HTTPException, status


from backend.api.vacancies.repository import get_vacancy_repo, get_vacancy_by_id
from backend.api.vacancies.schemas import VacancySchema, VacancyAddSchema
from backend.api.users.auth.token_dependencies import get_user_by_token
from backend.api.users.employers.dependencies import get_employer_by_token
from backend.api.users.employers.repository import get_employer_repo
from backend.api.users.employers.schemas import EmployerSchema


async def get_vacancy_by_id_dependencies(
        vacancy_id: int,
        user=Depends(get_user_by_token)
):
    can_update = True
    vacancy = await get_vacancy_by_id(vacancy_id)
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='vacancy is not exist'
        )
    if not (hasattr(user, 'company_id') and hasattr(user, 'is_owner')):
        can_update = False
    elif user.company_id != vacancy.company_id:
        can_update = False
    return vacancy, user, can_update


async def create_vacancy_dependencies(
        vacancy: VacancyAddSchema,
        owner: EmployerSchema = Depends(get_employer_by_token)
):
    if not owner.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user dont have company'
        )
    vacancy_repo = get_vacancy_repo()
    vacancy = await vacancy_repo.add_one(title=vacancy.title, description=vacancy.description, salary_first=vacancy.salary_first,
                                         salary_second=vacancy.salary_second, city=vacancy.city, company_id=owner.company_id)
    return vacancy, owner


async def delete_vacancy_by_id_dependencies(
        vacancy_id: int,
        owner: EmployerSchema = Depends(get_employer_by_token)
):
    if not owner.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user dont have company'
        )
    vacancy_for_delete = await get_vacancy_by_id(vacancy_id)
    if owner.company_id != vacancy_for_delete.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user is not owner this company'
        )
    vacancy_repo = get_vacancy_repo()
    vacancy = await vacancy_repo.delete_one()
    return owner