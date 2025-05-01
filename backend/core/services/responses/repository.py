from sqlalchemy.ext.asyncio import AsyncSession


class ResponseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
