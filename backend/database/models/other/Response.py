from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.settings.database import Base


class ResponsesOrm(Base):
    __tablename__ = 'responses'

    vacancy_id: Mapped[int] = mapped_column(ForeignKey('vacancies.id', ondelete='CASCADE'))
    resume_id: Mapped[int] = mapped_column(ForeignKey('resumes.id', ondelete='CASCADE'))
    is_worker_accepted: Mapped[bool] = mapped_column(nullable=True, default=None)
    is_employer_accepted: Mapped[bool] = mapped_column(nullable=True, default=None)

    _table_args__ = (
        UniqueConstraint('vacancy_id', 'resume_id', name='uq_responses_vacancies'),
    )
    vacancy: Mapped['VacanciesOrm'] = relationship(
        'VacanciesOrm',
        back_populates='responses',
    )
    resume: Mapped['ResumesOrm'] = relationship(
        'ResumesOrm',
        back_populates='responses',
    )

