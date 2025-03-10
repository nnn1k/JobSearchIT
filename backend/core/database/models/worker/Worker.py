from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database.settings.database import Base


class WorkersOrm(Base):
    __tablename__ = 'workers'

    name: Mapped[str] = mapped_column(nullable=True)
    surname: Mapped[str] = mapped_column(nullable=True)
    patronymic: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str]
    phone: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[bytes]
    birthday: Mapped[date] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    is_confirmed: Mapped[bool] = mapped_column(default=False)

    resumes: Mapped[list['ResumesOrm']] = relationship(
        'ResumesOrm',
        back_populates='worker',
        lazy='noload',
    )
    educations: Mapped[list['EducationsOrm']] = relationship(
        'EducationsOrm',
        back_populates='worker',
        lazy='noload',
    )
