import httpx

from userlife.application.interfaces.llm import LLMResponse
from userlife.core.config import Settings


class LLMProviderError(RuntimeError):
    pass


class OllamaProvider:
    name = "ollama"

    def __init__(self, settings: Settings) -> None:
        self.base_url = settings.llm_ollama_base_url.rstrip("/")
        self.model = settings.llm_ollama_model
        self.timeout = settings.llm_timeout_seconds

    async def complete(self, messages: list[dict[str, str]]) -> LLMResponse:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json={"model": self.model, "messages": messages, "stream": False},
                )
                response.raise_for_status()
                text = response.json()["message"]["content"]
        except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
            raise LLMProviderError(f"Ollama failed: {exc}") from exc
        return LLMResponse(provider=self.name, model=self.model, text=text)


class GeminiProvider:
    name = "gemini"

    def __init__(self, settings: Settings) -> None:
        if not settings.llm_gemini_api_key:
            raise ValueError("Gemini API key is not configured")
        self.api_key = settings.llm_gemini_api_key
        self.model = settings.llm_gemini_model
        self.timeout = settings.llm_timeout_seconds

    async def complete(self, messages: list[dict[str, str]]) -> LLMResponse:
        prompt = "\n\n".join(f"{item['role']}: {item['content']}" for item in messages)
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent"
        )
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    params={"key": self.api_key},
                    json={"contents": [{"parts": [{"text": prompt}]}]},
                )
                response.raise_for_status()
                text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMProviderError(f"Gemini failed: {exc}") from exc
        return LLMResponse(provider=self.name, model=self.model, text=text)


class OpenRouterProvider:
    name = "openrouter"

    def __init__(self, settings: Settings) -> None:
        if not settings.llm_openrouter_api_key:
            raise ValueError("OpenRouter API key is not configured")
        self.api_key = settings.llm_openrouter_api_key
        self.model = settings.llm_openrouter_model
        self.site_url = settings.llm_openrouter_site_url
        self.app_name = settings.llm_openrouter_app_name
        self.timeout = settings.llm_timeout_seconds

    async def complete(self, messages: list[dict[str, str]]) -> LLMResponse:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "HTTP-Referer": self.site_url,
                        "X-Title": self.app_name,
                    },
                    json={"model": self.model, "messages": messages, "temperature": 0.2},
                )
                response.raise_for_status()
                text = response.json()["choices"][0]["message"]["content"]
        except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMProviderError(f"OpenRouter failed: {exc}") from exc
        return LLMResponse(provider=self.name, model=self.model, text=text)
