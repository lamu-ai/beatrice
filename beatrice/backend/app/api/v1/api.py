"""API routers."""

import fastapi

from app.api.v1 import anime
from app.api.v1 import book
from app.api.v1 import login
from app.api.v1 import manga
from app.api.v1 import movie
from app.api.v1 import patrons

api_router = fastapi.APIRouter()
api_router.include_router(anime.router, prefix="/anime", tags=["anime"])
api_router.include_router(book.router, prefix="/books", tags=["books"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(manga.router, prefix="/manga", tags=["manga"])
api_router.include_router(movie.router, prefix="/movies", tags=["movies"])
api_router.include_router(patrons.router, prefix="/patrons", tags=["patrons"])
