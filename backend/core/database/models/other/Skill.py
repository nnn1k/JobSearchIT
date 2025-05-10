from sqlalchemy.orm import Mapped, relationship

from backend.core.database.database import Base, intpk, created_at, updated_at


class SkillsOrm(Base):
    __tablename__ = 'skills'

    id: Mapped[intpk]
    name: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    resumes: Mapped[list['ResumesOrm']] = relationship(
        'ResumesOrm',
        secondary='resumes_skills',
        back_populates='skills',
        overlaps='resumes_skills'
    )
    vacancies: Mapped[list['VacanciesOrm']] = relationship(
        'VacanciesOrm',
        secondary='vacancies_skills',
        back_populates='skills',
        overlaps='vacancies_skills'
    )
