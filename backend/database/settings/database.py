import datetime
from typing import Annotated

from sqlalchemy import text, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from backend.utils.settings import settings
from backend.utils.other.logger_utils import logger

engine = create_async_engine(
    url=settings.db.url,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
)

def log_queries(conn, cursor, statement, parameters, context, executemany):
    logger.log('DATABASE', f"Executing: {statement} | Params: {parameters}\n")


event.listen(engine.sync_engine, 'before_cursor_execute', log_queries)
session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncSession:
    import time
    start_time = time.time()
    async with session_factory() as session:
        logger.log('DATABASE', f"Connection established in {time.time() - start_time:.2f} seconds")
        yield session
        await session.close()

class Base(DeclarativeBase):
    repr_cols_num = 10
    repr_cols = tuple()

    id: Mapped[Annotated[int, mapped_column(primary_key=True)]]

    created_at: Mapped[Annotated[
        datetime.datetime,
        mapped_column(
            server_default=text("CURRENT_TIMESTAMP + interval '3 hours'")
        )
    ]]

    updated_at: Mapped[Annotated[
        datetime.datetime,
        mapped_column(
            server_default=text("CURRENT_TIMESTAMP + interval '3 hours'"),
            onupdate=lambda: datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        )
    ]]

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')
        return f'<{self.__class__.__name__} {", ".join(cols)}>'
