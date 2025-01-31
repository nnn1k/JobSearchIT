from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from backend.database.settings.database import Base

class SkillsOrm(Base):
    __tablename__ = 'skills'

    name: Mapped[str]


class VacanciesSkillsOrm(Base):
    __tablename__ = 'vacancies_skills'

    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id', ondelete='CASCADE'))
    vacancy_id: Mapped[int] = mapped_column(ForeignKey('vacancies.id', ondelete='CASCADE'))


class WorkersSkillsOrm(Base):
    __tablename__ = 'workers_skills'

    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id', ondelete='CASCADE'))
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id', ondelete='CASCADE'))


class ResponsesOrm(Base):
    __tablename__ = 'responses'

    vacancy_id: Mapped[int] = mapped_column(ForeignKey('vacancies.id', ondelete='CASCADE'))
    resume_id: Mapped[int] = mapped_column(ForeignKey('resumes.id', ondelete='CASCADE'))
