from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database.database import Base, intpk, created_at, updated_at


class ProfessionsOrm(Base):
    __tablename__ = 'professions'

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(index=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

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
