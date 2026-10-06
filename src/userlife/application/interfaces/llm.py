from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LLMResponse:
    provider: str
    model: str
    text: str


class LLMProvider(Protocol):
    name: str
    model: str

    async def complete(self, messages: list[dict[str, str]]) -> LLMResponse:
        ...
