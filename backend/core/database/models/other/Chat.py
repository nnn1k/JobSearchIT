from backend.core.database.database import Base, intpk, created_at, updated_at
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ChatsOrm(Base):
    __tablename__ = 'chats'
    id: Mapped[intpk]

    response_id: Mapped[int] = mapped_column(ForeignKey('responses.id', ondelete='CASCADE'))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

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
