from fastapi import Depends, HTTPException, status

from backend.api.vacancies.repository import get_vacancy_repo, get_vacancy_by_id
from backend.api.vacancies.schemas import VacancySchema, VacancyAddSchema
from backend.api.users.auth.token_dependencies import get_user_by_token
from backend.api.users.employers.dependencies import get_employer_by_token
from backend.api.users.employers.repository import get_employer_repo
from backend.api.users.employers.schemas import EmployerSchema
from backend.utils.other.check_func import check_can_update


async def get_vacancy_by_id_dependencies(
        vacancy_id: int,
        user=Depends(get_user_by_token)
):
    vacancy = await get_vacancy_by_id(vacancy_id)
    can_update = check_can_update(user, vacancy)
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='vacancy is not exist'
        )
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
    vacancy = await vacancy_repo.add_one(company_id=owner.company_id, **vacancy.model_dump())
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
    vacancy = await vacancy_repo.soft_delete(vacancy_id)
    return vacancy, owner
