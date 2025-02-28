from sqlalchemy import Index
from sqlalchemy.orm import Mapped, relationship

from backend.database.models.worker import ResumesOrm
from backend.database.settings.database import Base

class ProfessionsOrm(Base):
    __tablename__ = 'professions'

    title: Mapped[str]
    vacancies: Mapped['VacanciesOrm'] = relationship(
        'VacanciesOrm',
        back_populates='profession',
        lazy='noload'
    )
    resumes: Mapped['ResumesOrm'] = relationship(
        'ResumesOrm',
        back_populates='profession',
        lazy='noload'
    )
    __table_args__ = (
        Index('idx_professions_title', 'title'),
    )


