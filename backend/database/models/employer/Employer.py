from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.models.employer.Company import CompaniesOrm
from backend.database.settings.database import Base


class EmployersOrm(Base):
    __tablename__ = 'employers'

    name: Mapped[str] = mapped_column(nullable=True)
    surname: Mapped[str] = mapped_column(nullable=True)
    patronymic: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str]
    phone: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[bytes]
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'), nullable=True)
    is_owner: Mapped[bool] = mapped_column(default=False)
    is_confirmed: Mapped[bool] = mapped_column(default=False)

    company: Mapped['CompaniesOrm'] = relationship(
        'CompaniesOrm',
        back_populates='employers',
        lazy='noload'
    )
