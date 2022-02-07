"""API routers."""

import fastapi

from app.api.v1 import anime, patrons

api_router = fastapi.APIRouter()
api_router.include_router(anime.router, prefix="/anime", tags=["anime"])
api_router.include_router(patrons.router, prefix="/patrons", tags=["patrons"])
