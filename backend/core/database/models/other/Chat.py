from backend.core.database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ChatsOrm(Base):
    __tablename__ = 'chats'

    response_id: Mapped[int] = mapped_column(ForeignKey('responses.id', ondelete='CASCADE'))

    messages: Mapped[list['MessagesOrm']] = relationship(
        'MessagesOrm',
        back_populates='chat',
        lazy='noload'
    )
    response: Mapped['ResponsesOrm'] = relationship(
        'ResponsesOrm',
        back_populates='chat',
        lazy='noload'
    )
