from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.responses.queries import (
    delete_response_queries,
    get_responses_queries,
    send_reaction_to_response,
    send_response_queries,
)
from backend.core.database.utils.dependencies import get_db
from backend.core.schemas.user_schema import UserResponseSchema
from backend.core.utils.auth_utils.user_login_dependencies import (
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
        reaction=accept,
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

@router.post('/{response_id}/accept', summary='Подтвердить отклик')
async def accept_invite_views(
        response_id: int,
        user: UserResponseSchema = Depends(get_user_by_token),
        session: AsyncSession = Depends(get_db),
):
    response = await send_reaction_to_response(user=user, session=session, response_id=response_id, reaction=True)
    return {
        'status': 'ok',
        'response': response,
    }

@router.post('/{response_id}/reject', summary='Отклонить отклик')
async def accept_invite_views(
        response_id: int,
        user: UserResponseSchema = Depends(get_user_by_token),
        session: AsyncSession = Depends(get_db),
):
    response = await send_reaction_to_response(user=user, session=session, response_id=response_id, reaction=False)
    return {
        'status': 'ok',
        'response': response,
    }

@router.delete('/{response_id}', summary='Удалить отклик')
async def delete_response_views(
        response_id: int,
        user: UserResponseSchema = Depends(get_user_by_token),
        session: AsyncSession = Depends(get_db),
):
    await delete_response_queries(user=user, session=session, response_id=response_id)
    return {
        'status': 'ok',
    }
