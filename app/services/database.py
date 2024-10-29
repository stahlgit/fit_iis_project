import contextlib
from os import getenv
from typing import AsyncIterator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

Base = declarative_base()  # Base class for models


class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
        self._engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )

    async def close(self):
        if self._engine is None:
            raise Exception("Database Session Manager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("Database Session Manager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncConnection]:
        if self._sessionmaker is None:
            raise Exception("Database Session Manager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # For testing purposes
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


database_url = getenv("DATABASE_URL")
if not database_url:
    raise Exception("Database URL is not set in the environment")

session_manager = DatabaseSessionManager()
session_manager.init(database_url)


async def get_db():
    async with session_manager.session() as session:
        yield session
