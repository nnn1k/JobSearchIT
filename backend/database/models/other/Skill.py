from sqlalchemy.orm import Mapped, relationship

from backend.database.settings.database import Base


class SkillsOrm(Base):
    __tablename__ = 'skills'

    name: Mapped[str]

    workers: Mapped[list['WorkersOrm']] = relationship(
        'WorkersOrm',
        secondary='workers_skills',
        back_populates='skills',
        overlaps='workers_skills'
    )
    vacancies: Mapped[list['VacanciesOrm']] = relationship(
        'VacanciesOrm',
        secondary='vacancies_skills',
        back_populates='skills',
        overlaps='vacancies_skills'
    )
