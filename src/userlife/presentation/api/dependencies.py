from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from userlife.application.services.health import HealthService
from userlife.application.services.life_items import LifeItemService
from userlife.infrastructure.db.health_repository import HealthRepository
from userlife.infrastructure.db.repositories.life_items import LifeItemRepository
from userlife.infrastructure.db.session import get_session


async_session = Annotated[AsyncSession, Depends(get_session)]


def get_health_service() -> HealthService:
    return HealthService(HealthRepository())


health_service = Annotated[HealthService, Depends(get_health_service)]


def get_life_item_service() -> LifeItemService:
    return LifeItemService(LifeItemRepository())


life_item_service = Annotated[LifeItemService, Depends(get_life_item_service)]
