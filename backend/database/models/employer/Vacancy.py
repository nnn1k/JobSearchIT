from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from backend.database.settings.database import Base

class VacanciesOrm(Base):
    __tablename__ = 'vacancies'

    title: Mapped[str]
    description: Mapped[str]
    salary_first: Mapped[int] = mapped_column(nullable=True)
    salary_second: Mapped[int] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id', ondelete='CASCADE'))

    company: Mapped['CompaniesOrm'] = relationship('CompaniesOrm', back_populates='vacancies')
    skills: Mapped[list['SkillsOrm']] = relationship(
        'SkillsOrm',
        secondary='vacancies_skills',
        back_populates='vacancies',
        overlaps='vacancies_skills'
    )