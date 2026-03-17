from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from config import settings


DSN = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
engine = create_async_engine(DSN)

local_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db():
    async with local_session() as session:
        yield session


Base = declarative_base()
