from fastapi import FastAPI

from userlife.core.config import get_settings
from userlife.core.logging import configure_logging
from userlife.presentation.api.routes.health import router as health_router
from userlife.presentation.api.routes.life_items import router as life_items_router
from userlife.presentation.api.routes.assistant import router as assistant_router
from userlife.presentation.api.routes.assistant_history import router as assistant_history_router


settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(life_items_router)
app.include_router(assistant_router)
app.include_router(assistant_history_router)
