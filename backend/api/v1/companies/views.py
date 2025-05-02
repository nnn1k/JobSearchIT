from fastapi import Depends, APIRouter
from backend.core.schemas.models.employer.company_schema import CompanyAddSchema, CompanyUpdateSchema
from backend.core.schemas.models.other.review_schema import ReviewCreate
from backend.core.schemas.models.worker.worker_schema import WorkerSchema
from backend.core.services.companies.dependencies import get_company_serv
from backend.core.services.companies.service import CompanyService
from backend.core.utils.auth_utils.user_login_dependencies import get_employer_by_token, get_user_by_token, \
    get_worker_by_token
from backend.core.schemas import EmployerSchema
from backend.core.utils.auth_utils.check_func import check_employer_can_update
from backend.core.utils.other.type_utils import UserVar

router = APIRouter(prefix='/companies', tags=['companies'])


@router.post('', summary='Создать компанию')
async def create_new_company(
        new_company: CompanyAddSchema,
        user: EmployerSchema = Depends(get_employer_by_token),
        company_serv: CompanyService = Depends(get_company_serv),
):
    new_company = await company_serv.create_company(new_company=new_company, employer=user)
    return {
        'company': new_company,
    }


@router.get('/{company_id}', summary='Посмотреть информацию о компании')
async def get_info_on_company(
        company_id: int,
        user: UserVar = Depends(get_user_by_token),
        company_serv: CompanyService = Depends(get_company_serv),
):
    company = await company_serv.get_company_rel(company_id=company_id)
    can_update = check_employer_can_update(user, company)
    return {
        'can_update': can_update,
        'company': company,
    }


@router.put('/{company_id}', summary='Изменить описание компании')
async def update_company(
        new_company: CompanyUpdateSchema,
        company_id: int,
        user: EmployerSchema = Depends(get_employer_by_token),
        company_serv: CompanyService = Depends(get_company_serv),
):
    company = await company_serv.update_company(company_id=company_id, employer=user, **new_company.model_dump())
    return {
        'company': company,
    }


@router.delete('/{company_id}', summary='Удалить компанию')
async def delete_company(
        company_id: int,
        user: EmployerSchema = Depends(get_employer_by_token),
        company_serv: CompanyService = Depends(get_company_serv),
):
    await company_serv.delete_company(company_id=company_id, employer=user)
    return {
        'status': 'ok'
    }


@router.post('/{company_id}/reviews', summary='Написать отзыв')
async def create_review(
        company_id: int,
        new_review: ReviewCreate,
        user: WorkerSchema = Depends(get_worker_by_token),
        company_serv: CompanyService = Depends(get_company_serv),
):
    review = await company_serv.add_review(worker=user, company_id=company_id, new_review=new_review)
    return {
        'review': review,
    }


@router.get('/{company_id}/reviews/{review_id}', summary='Посмотреть отзыв')
async def get_review(
        company_id: int,
        review_id: int,
        user: UserVar = Depends(get_user_by_token),
        company_serv: CompanyService = Depends(get_company_serv),
):
    review = await company_serv.get_review(company_id=company_id, review_id=review_id)
    can_update = False
    if user:
        if user.id == review.worker_id:
            can_update = True
    return {
        'review': review,
        'can_update': can_update,
    }

@router.get('/{company_id}/reviews', summary='Посмотреть все отзывы у компании')
async def get_reviews(
        company_id: int,
        user: UserVar = Depends(get_user_by_token),
        company_serv: CompanyService = Depends(get_company_serv),
):
    reviews = await company_serv.get_reviews(company_id=company_id)
    return {
        'reviews': reviews,
    }

@router.post('/{company_id}/reviews/{review_id}', summary='Изменить отзыв')
async def update_review(
        company_id: int,
        review_id: int,
        new_review: ReviewCreate,
        worker: WorkerSchema = Depends(get_worker_by_token),
        company_serv: CompanyService = Depends(get_company_serv),
):
    review = await company_serv.update_review(
        worker=worker, company_id=company_id, review_id=review_id, new_review=new_review
    )
    return {
        'review': review,
    }


@router.delete('/{company_id}/reviews/{review_id}', summary='Удалить отзыв')
async def delete_review(
        company_id: int,
        review_id: int,
        worker: WorkerSchema = Depends(get_worker_by_token),
        company_serv: CompanyService = Depends(get_company_serv),
):
    await company_serv.delete_review(worker=worker, company_id=company_id, review_id=review_id)
    return {
        'status': 'ok'
    }

