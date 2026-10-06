from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_name: str = "userlife"
    log_level: str = "INFO"
    port: int = 8000
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/userlife"
    llm_enabled: bool = False
    llm_providers: str = "ollama,gemini,openrouter"
    llm_timeout_seconds: float = 30.0
    llm_ollama_base_url: str = "http://host.docker.internal:11434"
    llm_ollama_model: str = "llama3.2:3b"
    llm_gemini_api_key: str | None = None
    llm_gemini_model: str = "gemini-2.5-flash"
    llm_openrouter_api_key: str | None = None
    llm_openrouter_model: str = "openrouter/free"
    llm_openrouter_site_url: str = "http://localhost:8000"
    llm_openrouter_app_name: str = "userlife"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def sqlalchemy_database_url(self) -> str:
        """Return a URL using the async psycopg driver expected by SQLAlchemy."""
        url = self.database_url
        if url.startswith("postgres://"):
            return "postgresql+psycopg://" + url.removeprefix("postgres://")
        if url.startswith("postgresql://"):
            return "postgresql+psycopg://" + url.removeprefix("postgresql://")
        return url


@lru_cache
def get_settings() -> Settings:
    return Settings()
