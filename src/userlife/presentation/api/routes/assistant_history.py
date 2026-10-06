from fastapi import APIRouter, Query
from sqlalchemy import select

from userlife.application.dto.entities import AssistantMessageRead
from userlife.infrastructure.db.models import AssistantMessage
from userlife.presentation.api.dependencies import async_session


router = APIRouter(prefix="/api/v1/assistant")


@router.get("/messages", response_model=list[AssistantMessageRead])
async def list_messages(
    session: async_session,
    limit: int = Query(default=50, ge=1, le=100),
):
    result = await session.scalars(
        select(AssistantMessage)
        .order_by(AssistantMessage.created_at.desc())
        .limit(limit)
    )
    return list(result)
