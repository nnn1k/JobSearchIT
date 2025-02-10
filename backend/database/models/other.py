from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database.settings.database import Base

class SkillsOrm(Base):
    __tablename__ = 'skills'

    name: Mapped[str]

    vacancies_skills: Mapped[list['VacanciesSkillsOrm']] = relationship('VacanciesSkillsOrm', back_populates='skill')
    workers_skills: Mapped[list['WorkersSkillsOrm']] = relationship('WorkersSkillsOrm', back_populates='skill')
    workers: Mapped[list['WorkersOrm']] = relationship('WorkersOrm',
                                                     secondary='workers_skills',
                                                     back_populates='skills',
                                                     overlaps='workers_skills')
    vacancies: Mapped[list['VacanciesOrm']] = relationship('VacanciesOrm',
                                                           secondary='vacancies_skills',
                                                           back_populates='skills',
                                                           overlaps='vacancies_skills')

class VacanciesSkillsOrm(Base):
    __tablename__ = 'vacancies_skills'

    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id', ondelete='CASCADE'))
    vacancy_id: Mapped[int] = mapped_column(ForeignKey('vacancies.id', ondelete='CASCADE'))

    __table_args__ = (
        UniqueConstraint('skill_id', 'vacancy_id', name='uq_skills_vacancies'),
    )

    skill: Mapped[SkillsOrm] = relationship('SkillsOrm', back_populates='vacancies_skills',
                                            overlaps='vacancies')
    vacancy: Mapped['VacanciesOrm'] = relationship('VacanciesOrm', back_populates='vacancies_skills',
                                                   overlaps='skills')


class WorkersSkillsOrm(Base):
    __tablename__ = 'workers_skills'

    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id', ondelete='CASCADE'))
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id', ondelete='CASCADE'))

    __table_args__ = (
        UniqueConstraint('skill_id', 'worker_id', name='uq_skills_workers'),
    )

    worker: Mapped['WorkersOrm'] = relationship('WorkersOrm', back_populates='workers_skills',
                                              overlaps='skills')
    skill: Mapped[SkillsOrm] = relationship('SkillsOrm', back_populates='workers_skills',
                                            overlaps='workers')


class ResponsesOrm(Base):
    __tablename__ = 'responses'

    vacancy_id: Mapped[int] = mapped_column(ForeignKey('vacancies.id', ondelete='CASCADE'))
    resume_id: Mapped[int] = mapped_column(ForeignKey('resumes.id', ondelete='CASCADE'))

    _table_args__ = (
        UniqueConstraint('vacancy_id', 'resume_id', name='uq_responses_vacancies'),
    )
