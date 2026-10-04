from sqlalchemy.ext.asyncio import AsyncSession

from userlife.infrastructure.db.health_repository import HealthRepository


class HealthService:
    def __init__(self, repository: HealthRepository) -> None:
        self.repository = repository

    async def check(self, session: AsyncSession) -> int:
        return await self.repository.check(session)
