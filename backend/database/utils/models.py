from sqlalchemy.orm import Mapped

from backend.database.settings.database import Base


class UsersAl(Base):
    __tablename__ = 'users'

    nickname: Mapped[str]

