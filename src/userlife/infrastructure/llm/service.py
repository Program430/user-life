import logging

from userlife.application.interfaces.llm import LLMProvider, LLMResponse
from userlife.core.config import Settings
from userlife.infrastructure.llm.providers import (
    GeminiProvider,
    LLMProviderError,
    OllamaProvider,
    OpenRouterProvider,
)


logger = logging.getLogger(__name__)


class NoLLMProviderAvailable(RuntimeError):
    pass


class FallbackLLM:
    def __init__(self, settings: Settings) -> None:
        self.providers = self._build_providers(settings)

    @staticmethod
    def _build_providers(settings: Settings) -> list[LLMProvider]:
        factories = {
            "ollama": lambda: OllamaProvider(settings),
            "gemini": lambda: GeminiProvider(settings),
            "openrouter": lambda: OpenRouterProvider(settings),
        }
        providers: list[LLMProvider] = []
        for name in settings.llm_providers.split(","):
            factory = factories.get(name.strip().lower())
            if factory is None:
                continue
            try:
                providers.append(factory())
            except ValueError:
                logger.info("Skipping unavailable LLM provider: %s", name.strip())
        return providers

    async def complete(self, messages: list[dict[str, str]]) -> LLMResponse:
        if not self.providers:
            raise NoLLMProviderAvailable("No LLM provider is configured")
        errors: list[str] = []
        for provider in self.providers:
            try:
                return await provider.complete(messages)
            except LLMProviderError as exc:
                errors.append(str(exc))
                logger.warning("LLM provider %s failed; trying fallback", provider.name)
        raise NoLLMProviderAvailable("; ".join(errors))
