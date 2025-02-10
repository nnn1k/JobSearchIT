from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.settings.database import Base


class ResumesOrm(Base):
    __tablename__ = 'resumes'

    title: Mapped[str]
    description: Mapped[str]
    salary_first: Mapped[int] = mapped_column(nullable=True)
    salary_second: Mapped[int] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    is_hidden: Mapped[bool] = mapped_column(default=False)
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id', ondelete='CASCADE'))

    worker: Mapped['WorkersOrm'] = relationship('WorkersOrm', back_populates='resumes')
