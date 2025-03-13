from sqlalchemy.orm import Mapped, relationship

from backend.core.database.database import Base


class CompaniesOrm(Base):
    __tablename__ = 'companies'

    name: Mapped[str]
    description: Mapped[str]

    employers: Mapped[list['EmployersOrm']] = relationship(
        'EmployersOrm',
        back_populates='company',
        lazy='noload'
    )
    vacancies: Mapped[list['VacanciesOrm']] = relationship(
        'VacanciesOrm',
        back_populates='company',
        lazy='noload'
    )
