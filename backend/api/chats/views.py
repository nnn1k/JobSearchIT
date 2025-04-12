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
active_users = dict()


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
                    print(active_connections)
                    if chat_id in active_connections:
                        for connection in active_connections[chat_id]:
                            if connection['user_id'] == user.id:
                                # Закрываем предыдущее подключение
                                await connection['ws'].close()
                                # Удаляем старое подключение из active_connections
                                active_connections[chat_id].remove(connection)
                                logger.info(f"Closed previous connection for user {user.id}")

                    # Добавляем новое подключение
                    if not active_connections.get(chat_id):
                        active_connections[chat_id] = []
                    active_connections[chat_id].append({'ws': ws, 'user_id': user.id, 'user_type': user.type})

                    # Отправляем историю сообщений
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
                        if connection['ws'].application_state == WebSocketState.CONNECTED:
                            await connection['ws'].send_json(response.model_dump_json())

                case 'leave':
                    # Удаляем подключение пользователя
                    active_connections[chat_id] = [conn for conn in active_connections[chat_id] if conn['ws'] != ws]

    except HTTPException as e:
        # Отправляем клиенту сообщение об ошибке
        await ws.send_text(json.dumps({
            "type": "error",
            "status_code": e.status_code,
            "detail": e.detail
        }))

    except WebSocketDisconnect:
        logger.info('disconnected')
        if chat_id in active_connections:
            active_connections[chat_id] = [conn for conn in active_connections[chat_id] if conn['ws'] != ws]
        if ws.client_state != WebSocketState.DISCONNECTED:
            await ws.close()

    finally:
        # Удаляем подключение пользователя при закрытии соединения
        if chat_id in active_connections:
            active_connections[chat_id] = [conn for conn in active_connections[chat_id] if conn['ws'] != ws]
        if ws.client_state != WebSocketState.DISCONNECTED:
            await ws.close()


@router.websocket('/ws')
async def chat_system_websocket(
        ws: WebSocket,
        user: UserResponseSchema = Depends(get_auth_user_by_token),
        session: AsyncSession = Depends(get_db)
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
                    chats = await get_all_chats_on_user(user=user, session=session)
                    response = {
                        'chats': [chat.model_dump_json() for chat in chats],
                        'type': 'open'
                    }
                    await ws.send_json(json.dumps(response))
                case 'join':
                    active_users[f'{user.id}:{user.type}'] = {'ws': ws, 'chat_id': chat_id, 'user': user}
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
                    # сохранение бд

                    await send_message_queries(user=user, chat_id=chat_id, message=message, session=session)
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