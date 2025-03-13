import json


from fastapi import APIRouter, Depends, Path, Query
from fastapi.websockets import WebSocket
from fastapi.websockets import WebSocketDisconnect, WebSocketState
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.chats.queries import get_all_messages_on_chat
from backend.core.database.utils.dependencies import get_db
from backend.core.schemas.models.other.chat_schema import ChatMessageSchema
from backend.core.schemas.user_schema import UserResponseSchema
from backend.core.utils.auth_utils.user_login_dependencies import get_auth_user_by_token

from backend.core.utils.logger_utils.logger_func import logger
router = APIRouter(prefix='/chats')

active_connections = {}


@router.websocket('/ws/{chat_id}')
async def chats_websocket(
        ws: WebSocket,
        user: UserResponseSchema = Depends(get_auth_user_by_token),
        chat_id: int = Path(..., gt=0),
        session: AsyncSession = Depends(get_db)
):

    await ws.accept()
    if chat_id not in active_connections:
        active_connections[chat_id] = []
    active_connections[chat_id].append(ws)
    logger.info(active_connections[chat_id])
    messages = await get_all_messages_on_chat(user=user, chat_id=chat_id, session=session)
    try:
        while True:

            # Получаем JSON-сообщение
            data = await ws.receive_json()

            logger.info(f"Received data: {data}")

            response = ChatMessageSchema(
                chat_id=chat_id,
                message=data.get("message"),
                sender_id=user.id,
                sender_type=user.type
            )
            for connection in active_connections[chat_id]:
                await connection.send_json(response.model_dump())

    except WebSocketDisconnect:
        active_connections[chat_id].remove(ws)
        if not active_connections[chat_id]:
            del active_connections[chat_id]
        logger.info('disconnected')

    finally:
        if ws.client_state != WebSocketState.DISCONNECTED:
            await ws.close()
