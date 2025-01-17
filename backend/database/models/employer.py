from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database.settings.database import Base

class EmployersOrm(Base):
    __tablename__ = 'employers'

    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str]
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'))
    is_owner: Mapped[bool]


class CompaniesOrm(Base):
    __tablename__ = 'companies'

    name: Mapped[str]
    description: Mapped[str]


class VacanciesOrm(Base):
    __tablename__ = 'vacancies'

    title: Mapped[str]
    description: Mapped[str]
    salary: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'))






