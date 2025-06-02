from fastapi import APIRouter, Depends

from backend.core.schemas.user_schema import UserResponseSchema
from backend.core.services.chats.dependencies import get_chat_serv
from backend.core.services.chats.service import ChatService
from backend.core.services.responses.dependencies import get_resp_serv
from backend.core.services.responses.service import ResponseService
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
        resp_serv: ResponseService = Depends(get_resp_serv),
):
    response = await resp_serv.send_response(user=user, resume_id=resume_id, vacancy_id=vacancy_id)
    return {
        'status': 'ok',
        'response': response,
    }


@router.post('/invite', summary='Отправить приглашение')
async def send_invite_views(
        vacancy_id: int,
        resume_id: int,
        user=Depends(get_employer_by_token),
        resp_serv: ResponseService = Depends(get_resp_serv),
):
    invite = await resp_serv.send_response(user=user, resume_id=resume_id, vacancy_id=vacancy_id)
    return {
        'status': 'ok',
        'invite': invite,
    }


@router.get('/response', summary='Посмотреть все отклики')
async def get_responses_worker_views(
        user: UserResponseSchema = Depends(get_auth_user_by_token),
        resp_serv: ResponseService = Depends(get_resp_serv),
):
    responses = await resp_serv.get_responses(user=user)

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
        resp_serv: ResponseService = Depends(get_resp_serv),
):
    responses = await resp_serv.get_invites(user=user)
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
        resp_serv: ResponseService = Depends(get_resp_serv),
        chat_serv: ChatService = Depends(get_chat_serv)
):
    response = await resp_serv.send_reaction(user=user, response_id=response_id, reaction=True)
    await chat_serv.create_chat(response_id=response_id)
    return {
        'status': 'ok',
        'response': response,
    }


@router.post('/{response_id}/reject', summary='Отклонить отклик/приглашение')
async def accept_invite_views(
        response_id: int,
        user: UserResponseSchema = Depends(get_auth_user_by_token),
        resp_serv: ResponseService = Depends(get_resp_serv)
):
    response = await resp_serv.send_reaction(user=user, response_id=response_id, reaction=False)
    return {
        'status': 'ok',
        'response': response,
    }


@router.delete('/{response_id}', summary='Удалить отклик/приглашение')
async def delete_response_views(
        response_id: int,
        user: UserResponseSchema = Depends(get_auth_user_by_token),
        resp_serv: ResponseService = Depends(get_resp_serv)
):

    await resp_serv.delete_response(response_id=response_id, user=user)
    return {
        'status': 'ok',
    }
