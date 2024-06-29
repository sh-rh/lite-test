from collections.abc import AsyncGenerator
from typing import Any
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[Any, Any]:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
