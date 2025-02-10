from sqlalchemy.orm import Mapped, relationship

from backend.database.settings.database import Base


class CompaniesOrm(Base):
    __tablename__ = 'companies'

    name: Mapped[str]
    description: Mapped[str]

    employers: Mapped[list['EmployersOrm']] = relationship('EmployersOrm', back_populates='company')
    vacancies: Mapped[list['VacanciesOrm']] = relationship('VacanciesOrm', back_populates='company')
