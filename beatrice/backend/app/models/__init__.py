"""Initialize the models package.

Imports the necessary models to resolve forward references.
See: https://github.com/tiangolo/sqlmodel/issues/121
"""

from app.models.anime import Anime, AnimeRead, AnimeReadWithPatron
from app.models.manga import Manga, MangaRead, MangaReadWithPatron
from app.models.movie import Movie, MovieRead, MovieReadWithPatron
from app.models.patron import Patron, PatronRead, PatronReadWithMedia

Anime.update_forward_refs(Patron=Patron)
Manga.update_forward_refs(Patron=Patron)
Movie.update_forward_refs(Patron=Patron)
Patron.update_forward_refs(Anime=Anime)
AnimeReadWithPatron.update_forward_refs(PatronRead=PatronRead)
MangaReadWithPatron.update_forward_refs(PatronRead=PatronRead)
MovieReadWithPatron.update_forward_refs(PatronRead=PatronRead)
PatronReadWithMedia.update_forward_refs(AnimeRead=AnimeRead,
                                        MangaRead=MangaRead,
                                        MovieRead=MovieRead)
