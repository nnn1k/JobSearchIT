from sqlalchemy.orm import Mapped, relationship

from backend.core.database.database import Base, intpk, created_at, updated_at


class CompaniesOrm(Base):
    __tablename__ = 'companies'

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    employers: Mapped[list['EmployersOrm']] = relationship(
        'EmployersOrm',
        back_populates='company',
        lazy='noload'
    )
    vacancies: Mapped[list['VacanciesOrm']] = relationship(
        'VacanciesOrm',
        back_populates='company',
        lazy='noload'
    )
    reviews: Mapped[list['ReviewsOrm']] = relationship(
        'ReviewsOrm',
        back_populates='company',
        lazy='noload'
    )
