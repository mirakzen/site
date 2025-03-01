import sys
from typing import Any

from common.config import cfg
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.sql import text

# from collections.abc import AsyncGenerator


_engine = create_async_engine(cfg.DB_CONNECTION_STRING)


async def get_session() -> AsyncSession:  # AsyncGenerator[AsyncSession, AsyncSession, AsyncSession] ???
    async with AsyncSession(_engine, expire_on_commit=False) as session:
        try:
            yield session
        except Exception:
            await session.rollback()


async def check_db() -> None:
    try:
        async with AsyncSession(_engine, expire_on_commit=False) as session:
            await session.execute(text("SELECT 1;"))
            cfg.logger.info("Successfully connected to database")
    except Exception as e:
        cfg.logger.error(f"Failed to connect to database: {str(e)}")
        sys.exit(1)


def get_model_dict(model: Any) -> dict[str, Any]:
    return {
        column.name: getattr(model, column.name) for column in model.__table__.columns
    }
