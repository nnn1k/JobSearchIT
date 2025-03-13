from pydantic import BaseModel


class ChatSchema(BaseModel):
    response_id: int
    message: list['MessageSchema']

class MessageSchema(BaseModel):
    chat_id: int
    message: str
    sender_id: int
    sender_type: str

    chat: 'ChatSchema'

class ChatMessageSchema(BaseModel):
    chat_id: int
    message: str
    sender_id: int
    sender_type: str
