from fastapi import APIRouter, HTTPException, status

from userlife.application.dto.entities import AssistantAskRequest, AssistantAskResponse
from userlife.application.services.assistant import AssistantService
from userlife.core.config import get_settings
from userlife.infrastructure.llm.service import FallbackLLM, NoLLMProviderAvailable
from userlife.presentation.api.dependencies import async_session


router = APIRouter(prefix="/api/v1/assistant")


def get_assistant_service() -> AssistantService:
    settings = get_settings()
    if not settings.llm_enabled:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM is disabled. Set LLM_ENABLED=true and configure a free provider.",
        )
    return AssistantService(FallbackLLM(settings))


@router.post("/ask", response_model=AssistantAskResponse)
async def ask_assistant(payload: AssistantAskRequest, session: async_session):
    service = get_assistant_service()
    try:
        reply, actions, result = await service.ask(session, payload.message)
    except NoLLMProviderAvailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No configured free LLM provider is available.",
        ) from exc
    return AssistantAskResponse(
        reply=reply,
        actions=actions,
        provider=result.provider,
        model=result.model,
    )
