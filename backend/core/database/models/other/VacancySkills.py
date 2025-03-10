from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database.settings.database import Base


class VacanciesSkillsOrm(Base):
    __tablename__ = 'vacancies_skills'

    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id', ondelete='CASCADE'))
    vacancy_id: Mapped[int] = mapped_column(ForeignKey('vacancies.id', ondelete='CASCADE'))

    __table_args__ = (
        UniqueConstraint('skill_id', 'vacancy_id', name='uq_skills_vacancies'),
    )
