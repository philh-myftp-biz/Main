from philh_myftp_biz.web.torrent import Torrent, TorrentFile, thePirateBay
from philh_myftp_biz.web.torrent import qBitTorrent as qbit
from philh_myftp_biz.web.torrent.models import EpisodeData
from philh_myftp_biz.functools import cached_property
from philh_myftp_biz.web import Omdb
from philh_myftp_biz.pc import Path
from typing import Callable
from sys import maxsize

try:
    from .weights import Weights
except ImportError:
    Weights = object()

#================================================

overrides = [
    Torrent(name=name, url=url, seeders=maxsize)
    for name, url in
    Path('E:/Plex/Torrenting/Overrides.json').JSON.Dict.items()
]

#================================================

class MediaItem:

    queries: list[str]
    """List of queries for the pirate bay"""

    paths: tuple[Path, Path]
    """Get the source and destination paths of the file"""

    finish: Callable[[], None] = lambda s: None
    """tasks to run after the download is complete"""

    dir: Path
    """Parent Folder"""

    weights: 'Weights' # pyright: ignore[reportInvalidTypeForm]

    file: None|TorrentFile = None

    torrent: None|Torrent = None

    @property
    def exists(self) -> bool:
        """Check if the destination file already exists"""
        return any(
            (self.weights(p) and p.size>0) for p in self.dir.children
        )

    def start(self, i:int=0) -> None:
        
        torrents: list[Torrent]
        match i:
            case 0: torrents = overrides
            case 1: torrents = qbit.queue.read()
            case 2: torrents = thePirateBay.search(*self.queries)
            case 3: return

        torrents = sorted(
            filter(self.weights, torrents),
            key = lambda m: -m.seeders
        )

        while torrents and (self.file is None):

            self.torrent = torrents.pop(0)
            self.torrent.start(stop_files=True)

            self.file = max(
                filter(
                    lambda f: self.weights(f) and f.path.type=='video',
                    self.torrent.files
                ),
                key = lambda f: f.size,
                default = None,
            )

        if self.file:
            self.file.start()
        else:
            MediaItem.start(self, i=i+1)

class Movie(MediaItem):

    dir = Path('E:/Plex/Media/Movies/')

    def __init__(self,
        title: str,
        year: int
    ) -> None:
        
        self.Title = title
        self.Year = year

        self.queries = [
            title,
            f'{title} {year}'
        ]

        self.weights = Weights(
            TITLE = [self.Title],
            YEAR = self.Year,
        )

    @cached_property
    def paths(self) -> tuple[Path, Path]:
        return (
            self.file.path, 
            self.dir.child(f"{self.Title} ({self.Year}).{self.file.path.ext}")
        )
    

class Show:

    dir = Path('E:/Plex/Media/Shows/')

    def __init__(self,
        title: str,
        year: int             
    ) -> None:

        self.Title = title
        self.Year = year

        self.dir = Show.dir.child(f"/{title} ({year})/")
        """../Media/Shows/{Title} ({Year})/"""

        self.omdb = Omdb.show(title, year)

        try:
            self.seasons = [Season(self, *i) for i in self.omdb.Seasons.items()]
        except IndexError:
            self.seasons = []

    @property
    def exists(self) -> bool:
        return all(s.exists for s in self.seasons)

    @cached_property
    def episodes(self) -> tuple['Episode', ...]:
        episodes = []
        for s in self.seasons:
            episodes += s.episodes
        return tuple(episodes)

class Season(MediaItem):

    def __init__(self,
        show: 'Show',
        season: str,
        episodes: dict[str, EpisodeData]
    ) -> None:
        
        self.show: Show = show
        self.num = int(season)

        self.dir = show.dir.child(f"/Season {self.num:02d}/")
        """E:/Plex/Media/Shows/{Show}/Season {Season}/"""

        self.dir.mkdir()

        self.queries = [
            self.show.Title,
            f'{self.show.Title} {self.show.Year}',
            f'{self.show.Title} Season {self.num}',
            f'{self.show.Title} s{self.num:02d}',
            f'{self.show.Title} s{self.num}',
            f'{self.show.Title} {self.num}',
        ]

        self.episodes = [Episode(self, i[1]) for i in episodes.items()]

        self.weights = Weights(
            TITLE = [self.show.Title],
            SEASON = self.num,
            EPISODE = None,
            YEAR = self.show.Year,
        )

    @property
    def exists(self) -> bool:
        return all(e.exists for e in self.episodes)
    
class Episode(MediaItem):

    def __init__(self,
        season: 'Season',
        episode: EpisodeData
    ) -> None:
        super().__init__()
        
        self.show: Show = season.show
        self.season: Season = season
        self.Title: str = episode.Title
        self.num = episode.Number

        self.dir = season.dir
        """E:/Plex/Media/Shows/{Show}/Season {Season}/"""

        self.queries = [
            self.show.Title,
            f'{self.show.Title} s{season.num:02d}e{self.num:02d}',
            f'{self.show.Title} {season.num:02d}x{self.num:02d}',
            f'{self.show.Title} {season.num}{self.num:02d}',
            f'{self.show.Title} {season.num} {self.num:02d}'
        ]

        self.weights = Weights(
            TITLE = [self.show.Title, self.Title, None],
            YEAR = self.show.Year,
            SEASON = season.num,
            EPISODE = self.num,
        )

    def start(self) -> None:
        self.torrent = self.season.torrent
        super().start()

    @cached_property
    def paths(self) -> tuple[Path, Path]:
        return (
            self.file.path,
            self.dir.child(f'/Season {self.season:02d} Episode {self.num:02d}.{self.file.path.ext}')
        )
    
