import datetime
from typing import Optional

from pydantic import BaseModel

from backend.core.schemas.global_schema import GlobalSchema


class ChatSchema(GlobalSchema):
    response_id: int
    messages: Optional[list['MessageSchema']]
    response: 'ResponseSchema'

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
