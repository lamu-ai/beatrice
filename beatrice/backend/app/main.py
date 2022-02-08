"""Main entrypoint of the application."""

import fastapi

from app.api.v1 import api
from app.core import config

app = fastapi.FastAPI(title=config.settings.APP_NAME,
                      openapi_url=f"{config.settings.API_V1_STR}/openapi.json")

app.include_router(api.api_router, prefix=config.settings.API_V1_STR)
