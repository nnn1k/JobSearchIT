from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database.settings.database import Base

class ResumesSkillsOrm(Base):
    __tablename__ = 'resumes_skills'

    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id', ondelete='CASCADE'))
    resume_id: Mapped[int] = mapped_column(ForeignKey('resumes.id', ondelete='CASCADE'))

    __table_args__ = (
        UniqueConstraint('skill_id', 'resume_id', name='uq_skills_resumes'),
    )

