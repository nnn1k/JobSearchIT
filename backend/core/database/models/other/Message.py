from backend.core.database.database import Base, intpk, created_at, updated_at
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MessagesOrm(Base):
    __tablename__ = 'messages'

    id: Mapped[intpk]
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id', ondelete='cascade'))
    message: Mapped[str]
    sender_id: Mapped[int]
    sender_type: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    chat: Mapped['ChatsOrm'] = relationship(
        'ChatsOrm',
        back_populates='messages',
        lazy='noload'
    )
