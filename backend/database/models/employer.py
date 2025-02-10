from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
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

    company: Mapped['CompaniesOrm'] = relationship('CompaniesOrm', back_populates='employers')

class CompaniesOrm(Base):
    __tablename__ = 'companies'

    name: Mapped[str]
    description: Mapped[str]

    employers: Mapped[list[EmployersOrm]] = relationship('EmployersOrm', back_populates='company')
    vacancies: Mapped[list['VacanciesOrm']] = relationship('VacanciesOrm', back_populates='company')

class VacanciesOrm(Base):
    __tablename__ = 'vacancies'

    title: Mapped[str]
    description: Mapped[str]
    salary_first: Mapped[int] = mapped_column(nullable=True)
    salary_second: Mapped[int] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id', ondelete='CASCADE'))

    company: Mapped[CompaniesOrm] = relationship('CompaniesOrm', back_populates='vacancies')
    vacancies_skills: Mapped[list['VacanciesSkillsOrm']] = relationship('VacanciesSkillsOrm',
                                                                        back_populates='vacancy',
                                                                      overlaps='skills')
    skills: Mapped[list['SkillsOrm']] = relationship('SkillsOrm',
                                                   secondary='vacancies_skills',
                                                   back_populates='vacancies',
                                                   overlaps='vacancies_skills')