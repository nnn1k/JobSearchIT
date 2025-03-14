import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

from backend.core.schemas.global_schema import GlobalSchema


class ChatSchema(GlobalSchema):
    response_id: int
    messages: Optional[list['MessageSchema']]
    last_message: Optional['MessageSchema'] = None
    response: 'ResponseSchema'

    @field_validator('messages', mode='after')
    def validate_messages(cls, messages: Optional[List['MessageSchema']]) -> Optional[List['MessageSchema']]:
        # Просто возвращаем messages, чтобы валидатор не пытался вернуть словарь
        return messages

    @model_validator(mode='after')
    def update_last_message(cls, values: 'ChatSchema') -> 'ChatSchema':
        # Обновляем last_message на основе messages
        if values.messages:
            values.last_message = values.messages[-1]
        else:
            values.last_message = None
        return values

class MessageSchema(GlobalSchema):
    chat_id: int
    message: str
    sender_id: int
    sender_type: str

    chat: Optional['ChatSchema']

class ChatMessageSchema(BaseModel):
    chat_id: int
    message: str
    sender_id: int
    sender_type: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    type: str = 'message'
