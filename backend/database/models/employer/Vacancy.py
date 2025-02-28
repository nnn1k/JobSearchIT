from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship


from backend.database.settings.database import Base

class VacanciesOrm(Base):
    __tablename__ = 'vacancies'

    profession_id: Mapped[int] = mapped_column(ForeignKey('professions.id'))
    description: Mapped[str]
    salary_first: Mapped[int] = mapped_column(nullable=True)
    salary_second: Mapped[int] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id', ondelete='CASCADE'))

    company: Mapped['CompaniesOrm'] = relationship(
        'CompaniesOrm',
        back_populates='vacancies',
        lazy='noload'
    )
    skills: Mapped[list['SkillsOrm']] = relationship(
        'SkillsOrm',
        secondary='vacancies_skills',
        back_populates='vacancies',
        overlaps='vacancies_skills',
        lazy='noload'
    )
    profession: Mapped['ProfessionsOrm'] = relationship(
        'ProfessionsOrm',
        back_populates='vacancies',
        lazy='noload'
    )
    __table_args__ = (
        Index('idx_vacancies_city', 'city'),
        Index('idx_vacancies_salary', 'salary_first')
    )