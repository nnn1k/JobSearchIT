from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.settings.database import Base

class WorkersSkillsOrm(Base):
    __tablename__ = 'workers_skills'

    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id', ondelete='CASCADE'))
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id', ondelete='CASCADE'))

    __table_args__ = (
        UniqueConstraint('skill_id', 'worker_id', name='uq_skills_workers'),
    )
