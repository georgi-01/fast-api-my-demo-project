import pytest_asyncio
from sqlalchemy import text

from tests.database import TestSessionLocal


@pytest_asyncio.fixture
async def session():
    async with TestSessionLocal() as session:
        yield session

        await session.rollback()

        await session.execute(text("TRUNCATE TABLE enrollment, exam, course, student, teacher, person CASCADE"))

        await session.commit()