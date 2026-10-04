from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from userlife.application.services.health import HealthService
from userlife.infrastructure.db.health_repository import HealthRepository
from userlife.infrastructure.db.session import get_session


async_session = Annotated[AsyncSession, Depends(get_session)]


def get_health_service() -> HealthService:
    return HealthService(HealthRepository())


health_service = Annotated[HealthService, Depends(get_health_service)]
