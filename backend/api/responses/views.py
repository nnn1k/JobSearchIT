
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.responses.queries import (
    get_responses_queries,
    send_response_queries
)
from backend.database.utils.dependencies import get_db
from backend.schemas.user_schema import UserAbstractSchema, UserResponseSchema
from backend.utils.auth_utils.user_login_dependencies import (
    get_user_by_token
)

router = APIRouter(prefix='/responses', tags=['responses'])


@router.post('', summary='Отправить/изменить отклик')
async def send_response_views(
        vacancy_id: int,
        resume_id: int,
        user=Depends(get_user_by_token),
        accept: Optional[bool] = True,
        session: AsyncSession = Depends(get_db)
):
    response = await send_response_queries(
        user=user,
        vacancy_id=vacancy_id,
        resume_id=resume_id,
        accept=accept,
        session=session
    )
    return {
        'response': response,
    }


@router.get('/response', summary='Посмотреть все отклики')
async def get_responses_worker_views(
        user: UserResponseSchema = Depends(get_user_by_token),
        session: AsyncSession = Depends(get_db),
):
    responses = await get_responses_queries(user=user, session=session, response=True)
    return {
        'status': 'ok',
        'all': responses,
        'accepted': [response for response in responses if response.is_employer_accepted is True],
        'rejected': [response for response in responses if response.is_employer_accepted is False],
        'waiting': [response for response in responses if response.is_employer_accepted is None],
    }


@router.get('/invite', summary='Посмотреть все приглашения')
async def get_invite_views(
        user: UserResponseSchema = Depends(get_user_by_token),
        session: AsyncSession = Depends(get_db),
):
    responses = await get_responses_queries(user=user, session=session, response=False)
    return {
        'status': 'ok',
        'all': responses,
        'accepted': [response for response in responses if response.is_worker_accepted is True],
        'rejected': [response for response in responses if response.is_worker_accepted is False],
        'waiting': [response for response in responses if response.is_worker_accepted is None],
    }
