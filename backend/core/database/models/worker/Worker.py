from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database.database import Base, intpk, created_at, updated_at


class WorkersOrm(Base):
    __tablename__ = 'workers'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=True)
    surname: Mapped[str] = mapped_column(nullable=True)
    patronymic: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str]
    phone: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[bytes]
    birthday: Mapped[date] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    is_confirmed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    resumes: Mapped[list['ResumesOrm']] = relationship(
        'ResumesOrm',
        back_populates='worker',
        lazy='noload',
    )
