"""API routers."""

import fastapi

from app.api.v1 import patrons

api_router = fastapi.APIRouter()
api_router.include_router(patrons.router, prefix="/patrons", tags=["patrons"])
