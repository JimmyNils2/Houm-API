from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

db_host = "localhost"
db_user = "postgres"
db_name = "houm"
db_password = "postgres"
db_port = 5432

ASYNC_SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)


async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, echo=True)



Async_SessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_async_db():
    async with Async_SessionLocal() as db:
        yield db
        await db.commit()
