from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from userlife.infrastructure.db.base import Base


class LifeItemRepository:
    async def create(self, session: AsyncSession, model: type[Base], values: dict[str, Any]) -> Base:
        entity = model(**values)
        session.add(entity)
        await session.commit()
        await session.refresh(entity)
        return entity

    async def list(
        self,
        session: AsyncSession,
        model: type[Base],
        limit: int = 50,
    ) -> list[Base]:
        result = await session.scalars(
            select(model).order_by(model.created_at.desc()).limit(limit)
        )
        return list(result)
