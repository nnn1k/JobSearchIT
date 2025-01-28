from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database.settings.database import Base

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


class ResumesOrm(Base):
    __tablename__ = 'resumes'

    title: Mapped[str]
    description: Mapped[str]
    salary_first: Mapped[int] = mapped_column(nullable=True)
    salary_second: Mapped[int] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    is_hidden: Mapped[bool] = mapped_column(default=False)
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id'))


class EducationsOrm(Base):
    __tablename__ = 'educations'

    education_type: Mapped[str]
    end_date: Mapped[str]
    institution: Mapped[str]
    specialization: Mapped[str]
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id'))
