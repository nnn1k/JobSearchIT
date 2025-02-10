from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.settings.database import Base


class ResponsesOrm(Base):
    __tablename__ = 'responses'

    vacancy_id: Mapped[int] = mapped_column(ForeignKey('vacancies.id', ondelete='CASCADE'))
    resume_id: Mapped[int] = mapped_column(ForeignKey('resumes.id', ondelete='CASCADE'))

    _table_args__ = (
        UniqueConstraint('vacancy_id', 'resume_id', name='uq_responses_vacancies'),
    )
