from fastapi import FastAPI

from userlife.core.config import get_settings
from userlife.core.logging import configure_logging
from userlife.presentation.api.routes.health import router as health_router


settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(title=settings.app_name)
app.include_router(health_router)
