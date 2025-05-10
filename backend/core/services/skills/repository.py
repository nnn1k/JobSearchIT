from sqlalchemy.ext.asyncio import AsyncSession


class SkillRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
