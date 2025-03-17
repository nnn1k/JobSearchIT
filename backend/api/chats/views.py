import json


from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi.websockets import WebSocket
from fastapi.websockets import WebSocketDisconnect, WebSocketState
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.chats.queries import get_all_chats_on_user, get_all_messages_on_chat, send_message_queries
from backend.core.database.utils.dependencies import get_db
from backend.core.schemas.models.other.chat_schema import ChatMessageSchema
from backend.core.schemas.user_schema import UserResponseSchema
from backend.core.utils.auth_utils.user_login_dependencies import get_auth_user_by_token

from backend.core.utils.logger_utils.logger_func import logger

from datetime import datetime

from backend.core.utils.other.time_utils import current_time

router = APIRouter(prefix='/chats', tags=['chats'])

active_connections = {}

@router.get('', summary='Получить все чаты')
async def get_all_chats(
        user: UserResponseSchema = Depends(get_auth_user_by_token),
        session: AsyncSession = Depends(get_db),
):
    chats = await get_all_chats_on_user(user=user, session=session)
    return {
        'status': 'ok',
        'chats': chats
    }


@router.websocket('/ws/{chat_id}')
async def chats_websocket(
        ws: WebSocket,
        chat_id: int,
        user: UserResponseSchema = Depends(get_auth_user_by_token),
        session: AsyncSession = Depends(get_db)
):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()

            logger.info(f"Received data: {data}")
            message_type = data.get('type')
            message = data.get('message')
            match message_type:
                case 'join':
                    if not active_connections.get(chat_id):
                        active_connections[chat_id] = []
                    active_connections[chat_id].append(ws)
                    messages = await get_all_messages_on_chat(user=user, chat_id=chat_id, session=session)
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

                    await send_message_queries(user=user, chat_id=chat_id, message=message, session=session)
                    for connection in active_connections[chat_id]:
                        if connection.application_state == WebSocketState.CONNECTED:
                            await connection.send_json(response.model_dump_json())

                case 'leave':
                    del active_connections[chat_id][ws]

    except HTTPException as e:
        # Отправляем клиенту сообщение об ошибке
        await ws.send_text(json.dumps({
            "type": "error",
            "status_code": e.status_code,
            "detail": e.detail
        }))
    except WebSocketDisconnect:
        logger.info('disconnected')

    finally:
        await ws.close()
