import datetime
from typing import Annotated

from sqlalchemy import text, event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from backend.utils.other.logger_utils import logger

from backend.database.settings.config import settings

engine = create_async_engine(
    url=settings.ASYNC_DB_URL,
    echo=False
)

def log_queries(conn, cursor, statement, parameters, context, executemany):
    logger.log('DATABASE',f"Executing: {statement} | Params: {parameters}\n")


event.listen(engine.sync_engine, 'before_cursor_execute', log_queries)
session_factory = async_sessionmaker(engine)

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
    deleted_at: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')
        return f'<{self.__class__.__name__} {", ".join(cols)}>'
