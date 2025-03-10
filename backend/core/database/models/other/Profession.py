from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database.settings.database import Base

class ProfessionsOrm(Base):
    __tablename__ = 'professions'

    title: Mapped[str] = mapped_column(index=True)
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



