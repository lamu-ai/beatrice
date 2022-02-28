"""API routers."""

import fastapi

from app.api.v1 import anime, login, manga, patrons

api_router = fastapi.APIRouter()
api_router.include_router(anime.router, prefix="/anime", tags=["anime"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(manga.router, prefix="/manga", tags=["manga"])
api_router.include_router(patrons.router, prefix="/patrons", tags=["patrons"])
