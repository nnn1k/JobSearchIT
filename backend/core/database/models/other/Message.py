from backend.core.database.settings.database import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

class MessagesOrm(Base):
    __tablename__ = 'messages'

    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id', ondelete='cascade'))
    message: Mapped[str]
    sender_id: Mapped[int]
    sender_type: Mapped[str]

    chat: Mapped['ChatsOrm'] = relationship(
        'ChatsOrm',
        back_populates='messages'
    )
