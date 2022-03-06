"""Main entrypoint of the application."""

import fastapi
from fastapi.middleware import cors

from app.api.v1 import api
from app.core import config

app = fastapi.FastAPI(title=config.settings.APP_NAME,
                      openapi_url=f"{config.settings.API_V1_STR}/openapi.json")
app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.api_router, prefix=config.settings.API_V1_STR)
