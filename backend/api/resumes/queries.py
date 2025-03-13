from sqlalchemy import and_, desc, select
from sqlalchemy.orm import selectinload

from backend.core.database.models.other import ProfessionsOrm
from backend.core.database.models.worker import ResumesOrm
from backend.core.database.database import session_factory
from backend.core.schemas import ResumeSchema
from backend.core.utils.const import WORKER_USER_TYPE


async def get_all_resumes_query(user, **kwargs):
    async with session_factory() as session:
        stmt = (
            select(ResumesOrm)
            .join(ProfessionsOrm)
            .options(selectinload(ResumesOrm.profession))
        )
        max_salary: int = kwargs.get("max_salary", None)
        profession: str = kwargs.get("profession", None)
        city: str = kwargs.get("city", None)
        if isinstance(city, str):
            city = city.strip()
        if isinstance(profession, str):
            profession = profession.strip()
        conditions = []
        if city:
            conditions.append(ResumesOrm.city == city)
        if max_salary:
            conditions.append(ResumesOrm.salary_second <= max_salary)
        if profession:
            conditions.append(ProfessionsOrm.title.ilike(f'%{profession}%'))
        if user:
            if user.type == WORKER_USER_TYPE:
                ...
                #conditions.append(ResumesOrm.worker_id != user.id)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = stmt.order_by(desc(ResumesOrm.updated_at))
        result = await session.execute(stmt)
        resumes = result.scalars().all()
        if not resumes:
            return list(), kwargs

        schemas = [ResumeSchema.model_validate(resume, from_attributes=True) for resume in resumes]
        return schemas, kwargs
