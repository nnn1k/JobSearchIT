from sqlalchemy.orm import Mapped, relationship

from backend.core.database.settings.database import Base


class SkillsOrm(Base):
    __tablename__ = 'skills'

    name: Mapped[str]

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
