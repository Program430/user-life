from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from userlife.infrastructure.db.base import Base
from userlife.infrastructure.db.repositories.life_items import LifeItemRepository


class LifeItemService:
    def __init__(self, repository: LifeItemRepository) -> None:
        self.repository = repository

    async def create(
        self,
        session: AsyncSession,
        model: type[Base],
        values: dict[str, Any],
    ) -> Base:
        return await self.repository.create(session, model, values)

    async def list(
        self,
        session: AsyncSession,
        model: type[Base],
        limit: int,
    ) -> list[Base]:
        return await self.repository.list(session, model, limit)
