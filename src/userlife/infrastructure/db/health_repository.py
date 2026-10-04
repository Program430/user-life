from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class HealthRepository:
    async def check(self, session: AsyncSession) -> int:
        result = await session.execute(text("SELECT 1"))
        return int(result.scalar_one())
