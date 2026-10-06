import json
import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from userlife.application.dto.entities import AssistantAction
from userlife.application.interfaces.llm import LLMResponse
from userlife.infrastructure.db.models import AssistantMessage
from userlife.infrastructure.llm.service import FallbackLLM


logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are the Userlife personal assistant.
Answer in the user's language. Return ONLY valid JSON in this shape:
{"reply":"short helpful answer","actions":[{"type":"task","payload":{}}]}

Allowed action types: note, task, debt, event, idea.
Use an action only when the user clearly asks to save or remember something.
For a reminder use type task and payload with title, due_at, person, description.
For a debt use person, amount, currency, direction (i_owe or owed_to_me).
For an event use title, starts_at, ends_at, location, description.
Dates must be ISO 8601 when known. Never invent an amount, date, or person.
Actions are drafts and require user confirmation before being saved.
"""


class AssistantService:
    def __init__(self, llm: FallbackLLM) -> None:
        self.llm = llm

    async def ask(self, session: AsyncSession, message: str) -> tuple[str, list[AssistantAction], LLMResponse]:
        history_result = await session.scalars(
            select(AssistantMessage)
            .order_by(AssistantMessage.created_at.desc())
            .limit(10)
        )
        history = list(reversed(list(history_result)))
        session.add(AssistantMessage(role="user", content=message))
        await session.flush()

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend({"role": item.role, "content": item.content} for item in history)
        messages.append({"role": "user", "content": message})

        result = await self.llm.complete(messages)
        reply, actions = self._parse_response(result.text)
        session.add(
            AssistantMessage(
                role="assistant",
                content=reply,
                provider=result.provider,
                model=result.model,
            )
        )
        await session.commit()
        return reply, actions, result

    @staticmethod
    def _parse_response(text: str) -> tuple[str, list[AssistantAction]]:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`").removeprefix("json").strip()
        try:
            data: dict[str, Any] = json.loads(cleaned)
            reply = str(data.get("reply", ""))
            actions = [AssistantAction.model_validate(item) for item in data.get("actions", [])]
            return reply, actions
        except (ValueError, TypeError, json.JSONDecodeError):
            logger.warning("LLM returned non-structured response")
            return text.strip(), []
