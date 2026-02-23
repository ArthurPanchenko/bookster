from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

engine = create_async_engine(
    "postgresql+asyncpg://postgres:admin@localhost:5432/bookster_fastapi"
)

local_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db():
    async with local_session() as session:
        yield session

Base = declarative_base()