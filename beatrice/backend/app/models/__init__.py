"""Initialize the models package.

Imports the necessary models to resolve forward references.
See: https://github.com/tiangolo/sqlmodel/issues/121
"""

from app.models.patron import Patron, PatronRead, PatronReadWithMedia
from app.models.anime import Anime, AnimeRead, AnimeReadWithPatron

Patron.update_forward_refs(Anime=Anime)
Anime.update_forward_refs(Patron=Patron)
PatronReadWithMedia.update_forward_refs(AnimeRead=AnimeRead)
AnimeReadWithPatron.update_forward_refs(PatronRead=PatronRead)
