from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.settings.database import Base


class ResumesOrm(Base):
    __tablename__ = 'resumes'

    profession_id: Mapped[int] = mapped_column(ForeignKey('professions.id'))
    description: Mapped[str]
    salary_first: Mapped[int] = mapped_column(nullable=True)
    salary_second: Mapped[int] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    is_hidden: Mapped[bool] = mapped_column(default=False)
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id', ondelete='CASCADE'))

    worker: Mapped['WorkersOrm'] = relationship(
        'WorkersOrm',
        back_populates='resumes',
        lazy='noload'
    )
    skills: Mapped[list['SkillsOrm']] = relationship(
        'SkillsOrm',
        secondary='resumes_skills',
        back_populates='resumes',
        overlaps='resumes_skills',
        lazy='noload'
    )
    profession: Mapped['ProfessionsOrm'] = relationship(
        'ProfessionsOrm',
        back_populates='resumes',
        lazy='noload'
    )
