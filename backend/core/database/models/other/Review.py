from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database.database import Base, intpk, created_at, updated_at


class ReviewsOrm(Base):
    __tablename__ = 'reviews'

    id: Mapped[intpk]
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id', ondelete='CASCADE'))
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id', ondelete='CASCADE'))
    score: Mapped[int]
    message: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    company: Mapped['CompaniesOrm'] = relationship(
        'CompaniesOrm',
        back_populates='reviews',
        lazy='noload'
    )
