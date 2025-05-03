from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database.database import Base, intpk, created_at, updated_at


class VacanciesOrm(Base):
    __tablename__ = 'vacancies'
    id: Mapped[intpk]
    profession_id: Mapped[int] = mapped_column(ForeignKey('professions.id'))
    description: Mapped[str]
    salary_first: Mapped[int] = mapped_column(nullable=True, index=True)
    salary_second: Mapped[int] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id', ondelete='CASCADE'))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    __table_args__ = (
        UniqueConstraint('profession_id', 'company_id', name='uq_profession_company'),
    )

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
        lazy='selectin'
    )
    profession: Mapped['ProfessionsOrm'] = relationship(
        'ProfessionsOrm',
        back_populates='vacancies',
        lazy='joined'
    )
    responses: Mapped[list['ResponsesOrm']] = relationship(
        'ResponsesOrm',
        back_populates='vacancy',
        lazy='noload'
    )
