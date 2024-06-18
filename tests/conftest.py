import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


from db.db_setup import Base, ASYNC_SQLALCHEMY_DATABASE_URL

from db.db_setup import Base, ASYNC_SQLALCHEMY_DATABASE_URL
from db.models.employee import Employee


engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest.fixture(scope="session")
async def async_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session
    await engine.dispose()


