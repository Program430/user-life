import logging

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from userlife.presentation.api.dependencies import health_service, async_session


logger = logging.getLogger(__name__)
router = APIRouter()


class HealthResponse(BaseModel):
    status: str


class DatabaseHealthResponse(BaseModel):
    status: str
    db: int


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/health/db", response_model=DatabaseHealthResponse)
async def database_health(
    session: async_session,
    service: health_service,
) -> DatabaseHealthResponse:
    try:
        result = await service.check(session)
    except SQLAlchemyError:
        logger.exception("Database health check failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="database unavailable",
        ) from None

    return DatabaseHealthResponse(status="ok", db=result)
