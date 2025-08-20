from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from loguru import logger
from sqlalchemy.ext.asyncio import (
	AsyncSession,
	async_sessionmaker,
	create_async_engine,
)

from src.utility import get_cached_settings

global engine, session_factory


async def init_db():
	global engine, session_factory
	engine = create_async_engine(
		get_cached_settings().postgres_async_uri,
		echo=get_cached_settings().POSTGRES_ECHO,
		pool_size=get_cached_settings().DB_MAX_CONNECTIONS
	)
	session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def close_db():
	if engine:
		await engine.dispose()


@asynccontextmanager
async def async_database_context() -> AsyncGenerator[AsyncSession]:
	assert session_factory is not None, "engine is not initialized. Call init_db first."
	async with session_factory() as session:
		try:
			yield session
			await session.commit()
		except Exception as exc:
			logger.exception(
					"[database] caught an exception while in async_db_ctx: {};",
	                exc.__class__.__name__
			)
			await session.rollback()
			raise exc
		finally:
			await session.close()