from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from backend.database.settings.database import Base

class SkillsOrm(Base):
    __tablename__ = 'skills'

    name: Mapped[str]


class VacanciesSkillsOrm(Base):
    __tablename__ = 'vacancies_skills'

    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id', ondelete='CASCADE'))
    vacancy_id: Mapped[int] = mapped_column(ForeignKey('vacancies.id', ondelete='CASCADE'))

    __table_args__ = (
        UniqueConstraint('skill_id', 'vacancy_id', name='uq_skills_vacancies'),
    )


class WorkersSkillsOrm(Base):
    __tablename__ = 'workers_skills'

    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id', ondelete='CASCADE'))
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id', ondelete='CASCADE'))

    __table_args__ = (
        UniqueConstraint('skill_id', 'worker_id', name='uq_skills_workers'),
    )


class ResponsesOrm(Base):
    __tablename__ = 'responses'

    vacancy_id: Mapped[int] = mapped_column(ForeignKey('vacancies.id', ondelete='CASCADE'))
    resume_id: Mapped[int] = mapped_column(ForeignKey('resumes.id', ondelete='CASCADE'))

    _table_args__ = (
        UniqueConstraint('vacancy_id', 'resume_id', name='uq_responses_vacancies'),
    )
