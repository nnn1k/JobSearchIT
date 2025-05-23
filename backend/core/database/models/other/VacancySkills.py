from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database.database import Base, intpk, created_at, updated_at


class VacanciesSkillsOrm(Base):
    __tablename__ = 'vacancies_skills'
    id: Mapped[intpk]

    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id', ondelete='CASCADE'))
    vacancy_id: Mapped[int] = mapped_column(ForeignKey('vacancies.id', ondelete='CASCADE'))

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    __table_args__ = (
        UniqueConstraint('skill_id', 'vacancy_id', name='uq_skills_vacancies'),
    )
