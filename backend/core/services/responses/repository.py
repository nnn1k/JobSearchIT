from typing import Sequence

from sqlalchemy import insert, select, desc, and_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.core.database.models.employer import VacanciesOrm
from backend.core.database.models.other import ResponsesOrm
from backend.core.database.models.worker import ResumesOrm
from backend.core.utils.const import WORKER_USER_TYPE, EMPLOYER_USER_TYPE


class ResponseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def send_response(
            self,
            resume_id: int,
            vacancy_id: int,
            first: str,
            is_worker_accepted: bool = False,
            is_employer_accepted: bool = False,
    ) -> ResponsesOrm:
        stmt = (
            insert(ResponsesOrm)
            .values(
                resume_id=resume_id,
                vacancy_id=vacancy_id,
                first=first,
                is_worker_accepted=is_worker_accepted,
                is_employer_accepted=is_employer_accepted
            )
            .returning(ResponsesOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_response(self, **kwargs) -> ResponsesOrm:
        stmt = (
            select(ResponsesOrm)
            .filter_by(**kwargs)
            .options(joinedload(ResponsesOrm.resume))
            .options(joinedload(ResponsesOrm.vacancy))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_responses_worker(self, user_id: int) -> Sequence[ResponsesOrm]:
        stmt = (
            select(ResponsesOrm)
            .join(ResumesOrm)
            .where(
                and_(
                    ResumesOrm.worker_id == user_id,
                    ResponsesOrm.first == WORKER_USER_TYPE
                )
            )
            .order_by(desc(ResponsesOrm.updated_at))
            .options(joinedload(ResponsesOrm.resume).joinedload(ResumesOrm.profession))
            .options(joinedload(ResponsesOrm.resume).joinedload(ResumesOrm.worker))
            .options(joinedload(ResponsesOrm.resume).selectinload(ResumesOrm.skills))
            .options(joinedload(ResponsesOrm.vacancy).joinedload(VacanciesOrm.profession))
            .options(joinedload(ResponsesOrm.vacancy).joinedload(VacanciesOrm.company))
            .options(joinedload(ResponsesOrm.vacancy).selectinload(VacanciesOrm.skills))
            .options(joinedload(ResponsesOrm.chat))
        )

        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def get_responses_employer(self, company_id: int) -> Sequence[ResponsesOrm]:
        stmt = (
            select(ResponsesOrm)
            .join(VacanciesOrm)
            .where(
                and_(
                    VacanciesOrm.company_id == company_id,
                    ResponsesOrm.first == WORKER_USER_TYPE
                )
            )
            .order_by(desc(ResponsesOrm.updated_at))
            .options(joinedload(ResponsesOrm.resume).joinedload(ResumesOrm.profession))
            .options(joinedload(ResponsesOrm.resume).joinedload(ResumesOrm.worker))
            .options(joinedload(ResponsesOrm.resume).selectinload(ResumesOrm.skills))
            .options(joinedload(ResponsesOrm.vacancy).joinedload(VacanciesOrm.profession))
            .options(joinedload(ResponsesOrm.vacancy).joinedload(VacanciesOrm.company))
            .options(joinedload(ResponsesOrm.vacancy).selectinload(VacanciesOrm.skills))
            .options(joinedload(ResponsesOrm.chat))
        )

        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def get_invites_worker(self, user_id: int) -> Sequence[ResponsesOrm]:
        stmt = (
            select(ResponsesOrm)
            .join(ResumesOrm)
            .where(
                and_(
                    ResumesOrm.worker_id == user_id,
                    ResponsesOrm.first == EMPLOYER_USER_TYPE
                )
            )
            .order_by(desc(ResponsesOrm.updated_at))
            .options(joinedload(ResponsesOrm.resume).joinedload(ResumesOrm.profession))
            .options(joinedload(ResponsesOrm.resume).joinedload(ResumesOrm.worker))
            .options(joinedload(ResponsesOrm.resume).selectinload(ResumesOrm.skills))
            .options(joinedload(ResponsesOrm.vacancy).joinedload(VacanciesOrm.profession))
            .options(joinedload(ResponsesOrm.vacancy).joinedload(VacanciesOrm.company))
            .options(joinedload(ResponsesOrm.vacancy).selectinload(VacanciesOrm.skills))
            .options(joinedload(ResponsesOrm.chat))
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def get_invites_employer(self, company_id: int) -> Sequence[ResponsesOrm]:
        stmt = (
            select(ResponsesOrm)
            .join(VacanciesOrm)
            .where(
                and_(
                    VacanciesOrm.company_id == company_id,
                    ResponsesOrm.first == EMPLOYER_USER_TYPE
                )
            )
            .order_by(desc(ResponsesOrm.updated_at))
            .options(joinedload(ResponsesOrm.resume).joinedload(ResumesOrm.profession))
            .options(joinedload(ResponsesOrm.resume).joinedload(ResumesOrm.worker))
            .options(joinedload(ResponsesOrm.resume).selectinload(ResumesOrm.skills))
            .options(joinedload(ResponsesOrm.vacancy).joinedload(VacanciesOrm.profession))
            .options(joinedload(ResponsesOrm.vacancy).joinedload(VacanciesOrm.company))
            .options(joinedload(ResponsesOrm.vacancy).selectinload(VacanciesOrm.skills))
            .options(joinedload(ResponsesOrm.chat))
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def send_reaction_to_response_worker(self, response_id: int, reaction: bool):
        stmt = (
            update(ResponsesOrm)
            .where(and_(ResponsesOrm.id == response_id))
            .values(is_worker_accepted=reaction)
            .returning(ResponsesOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def send_reaction_to_response_employer(self, response_id: int, reaction: bool):
        stmt = (
            update(ResponsesOrm)
            .where(and_(ResponsesOrm.id == response_id))
            .values(is_employer_accepted=reaction)
            .returning(ResponsesOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def delete_response(self, response_id: int) -> ResponsesOrm:
        stmt = (
            delete(ResponsesOrm)
            .filter_by(id=response_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
