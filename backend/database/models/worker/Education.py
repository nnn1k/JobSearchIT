from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database.settings.database import Base


class EducationsOrm(Base):
    __tablename__ = 'educations'

    education_type: Mapped[str]
    end_date: Mapped[str]
    institution: Mapped[str]
    specialization: Mapped[str]
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id', ondelete='CASCADE'))

    worker: Mapped['WorkersOrm'] = relationship('WorkersOrm', back_populates='educations')