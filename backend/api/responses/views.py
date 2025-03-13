from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.chats.queries import create_chat_queries
from backend.api.responses.queries import (
    delete_response_queries,
    get_responses_queries,
    send_reaction_to_response,
    send_response_queries,
)

from backend.core.database.utils.dependencies import get_db
from backend.core.schemas.user_schema import UserResponseSchema
from backend.core.utils.auth_utils.user_login_dependencies import (
    get_auth_user_by_token,
    get_employer_by_token,
    get_worker_by_token
)

router = APIRouter(prefix='/responses', tags=['responses'])


@router.post('/response', summary='Отправить отклик')
async def send_response_views(
        vacancy_id: int,
        resume_id: int,
        user=Depends(get_worker_by_token),
        session: AsyncSession = Depends(get_db)
):
    response = await send_response_queries(
        user=user,
        vacancy_id=vacancy_id,
        resume_id=resume_id,
        session=session
    )
    return {
        'status': 'ok',
        'response': response,
    }

@router.post('/invite', summary='Отправить приглашение')
async def send_invite_views(
        vacancy_id: int,
        resume_id: int,
        user=Depends(get_employer_by_token),
        session: AsyncSession = Depends(get_db),
):
    invite = await send_response_queries(
        user=user,
        vacancy_id=vacancy_id,
        resume_id=resume_id,
        session=session
    )
    await create_chat_queries(response_id=invite.id, session=session)
    return {
        'status': 'ok',
        'invite': invite,
    }

@router.get('/response', summary='Посмотреть все отклики')
async def get_responses_worker_views(
        user: UserResponseSchema = Depends(get_auth_user_by_token),
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
        user: UserResponseSchema = Depends(get_auth_user_by_token),
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

@router.post('/{response_id}/accept', summary='Подтвердить отклик/приглашение')
async def accept_invite_views(
        response_id: int,
        user: UserResponseSchema = Depends(get_auth_user_by_token),
        session: AsyncSession = Depends(get_db),
):
    response = await send_reaction_to_response(user=user, session=session, response_id=response_id, reaction=True)
    return {
        'status': 'ok',
        'response': response,
    }

@router.post('/{response_id}/reject', summary='Отклонить отклик/приглашение')
async def accept_invite_views(
        response_id: int,
        user: UserResponseSchema = Depends(get_auth_user_by_token),
        session: AsyncSession = Depends(get_db),
):
    response = await send_reaction_to_response(user=user, session=session, response_id=response_id, reaction=False)
    return {
        'status': 'ok',
        'response': response,
    }

@router.delete('/{response_id}', summary='Удалить отклик/приглашение')
async def delete_response_views(
        response_id: int,
        user: UserResponseSchema = Depends(get_auth_user_by_token),
        session: AsyncSession = Depends(get_db),
):
    await delete_response_queries(user=user, session=session, response_id=response_id)
    return {
        'status': 'ok',
    }
