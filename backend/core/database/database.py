import datetime
from typing import Annotated

from sqlalchemy import text, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from backend.core.config.help_func import check_platform
from backend.core.config.settings import settings
from backend.core.utils.logger_utils.logger_func import logger

engine = create_async_engine(
    url=settings.db.url,
    echo=False,
)

check_platform()


def log_queries(conn, cursor, statement, parameters, context, executemany):
    logger.log('DATABASE', f"Executing: {statement} | Params: {parameters}\n")


event.listen(engine.sync_engine, 'before_cursor_execute', log_queries)
session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

intpk = Annotated[
    int,
    mapped_column(primary_key=True)
]

created_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("CURRENT_TIMESTAMP + interval '3 hours'"),
    )
]

updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("CURRENT_TIMESTAMP + interval '3 hours'"),
        onupdate=lambda: datetime.datetime.utcnow() + datetime.timedelta(hours=3),
    )
]


class Base(DeclarativeBase):
    repr_cols_num = 10
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')
        return f'<{self.__class__.__name__} {", ".join(cols)}>'
