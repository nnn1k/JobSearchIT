import json


from fastapi import APIRouter, Depends, HTTPException
from fastapi.websockets import WebSocket
from fastapi.websockets import WebSocketDisconnect, WebSocketState
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.utils.dependencies import get_db
from backend.core.schemas.models.other.chat_schema import ChatMessageSchema
from backend.core.schemas.user_schema import UserResponseSchema
from backend.core.services.chats.dependencies import get_chat_serv
from backend.core.services.chats.service import ChatService
from backend.core.utils.auth_utils.user_login_dependencies import get_auth_user_by_token

from backend.core.utils.logger_utils.logger_func import logger

from backend.core.utils.other.time_utils import current_time

router = APIRouter(prefix='/chats', tags=['chats'])

active_users = dict()

@router.websocket('/ws')
async def chat_system_websocket(
        ws: WebSocket,
        user: UserResponseSchema = Depends(get_auth_user_by_token),
        chat_serv: ChatService = Depends(get_chat_serv)
):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            logger.info(f"Received data: {data}")
            message = data.get('message')
            message_type = data.get('type')
            chat_id = data.get('chat_id')
            if chat_id:
                chat_id = int(chat_id)
            match message_type:
                case 'open':
                    chats = await chat_serv.get_all_chats(user=user)
                    response = {
                        'chats': [chat.model_dump_json() for chat in chats],
                        'type': 'open'
                    }
                    await ws.send_json(json.dumps(response))
                case 'join':
                    active_users[f'{user.id}:{user.type}'] = {'ws': ws, 'chat_id': chat_id, 'user': user}
                    messages = await chat_serv.get_all_messages(user=user, chat_id=chat_id)
                    response = {
                        'messages': [message.model_dump_json() for message in messages],
                        'type': 'join'
                    }
                    await ws.send_json(json.dumps(response))
                case 'message':
                    response = ChatMessageSchema(
                        chat_id=chat_id,
                        message=message,
                        sender_id=user.id,
                        sender_type=user.type,
                        created_at=current_time(),
                        updated_at=current_time()
                    )
                    # сохранение бд

                    await chat_serv.send_message(chat_id=chat_id, message=message, user=user)
                    # отправка пользователям
                    for key in active_users:
                        if active_users[key].get('chat_id') == chat_id:
                            await active_users[key].get('ws').send_json(response.model_dump_json())

    except HTTPException as e:
        await ws.send_text(json.dumps({
            "type": "error",
            "status_code": e.status_code,
            "detail": e.detail
        }))

    except WebSocketDisconnect:
        if ws.client_state != WebSocketState.DISCONNECTED:
            await ws.close()
            logger.info('disconnected')

    finally:
        if ws.client_state != WebSocketState.DISCONNECTED:
            await ws.close()