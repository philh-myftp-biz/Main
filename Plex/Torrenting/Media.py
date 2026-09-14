from philh_myftp_biz.web.torrent import Torrent, TorrentFile, thePirateBay
from philh_myftp_biz.functools import loc, attr, cached_property
from philh_myftp_biz.web.torrent import qBitTorrent as qbit
from philh_myftp_biz.web.torrent.models import EpisodeData
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

    weights: Weights
    torrent: None|Torrent = None

    @property
    def exists(self) -> bool:
        """Check if the destination file already exists"""
        return any(
            (self.weights(p) and p.size>0) for p in self.dir.children
        )

    @cached_property
    def file(self) -> None | TorrentFile:
        if self.torrent is None: return
        
        files: list[TorrentFile] = filter(
            lambda f: self.weights(f) and f.path.type=='video',
            self.torrent.files
        )

        return max(
            files,
            key = lambda f: f.size,
            default = None
        )

    def start(self, i:int=0) -> None:

        del self.file
        if self.file: 
            self.file.start()
            return
        
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

        for self.torrent in torrents:
            self.torrent.start(stop_files=True)
            del self.file
            if self.file: break

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

        self.omdb = Omdb.movie(title, year)

        self.weights = Weights(
            TITLE = [self.Title],
            YEAR = self.Year,
            UPLOADED = self.omdb.Released
        )

    @cached_property
    def paths(self) -> tuple[Path, Path]:
        return (
            self.file.path, 
            self.dir.child(f"{self.Title} ({self.Year}).{self.file.path.ext}")
        )
    
    def __repr__(self) -> str:
        return f'<Movie "{self.Title} ({self.Year})" @{loc(self)}>'

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

    def __repr__(self) -> str:
        return f'<Show "{self.Title}" @{loc(self)}>'

    @cached_property
    def episodes(self) -> tuple[Episode, ...]:
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

        attr(self, '__int__').set(lambda s: int(season))

        self.dir = show.dir.child(f"/Season {self:02d}/")
        """E:/Plex/Media/Shows/{Show}/Season {Season}/"""

        self.dir.mkdir()

        self.queries = [
            self.show.Title,
            f'{self.show.Title} {self.show.Year}',
            f'{self.show.Title} Season {self}',
            f'{self.show.Title} s{self:02d}',
            f'{self.show.Title} s{self}',
            f'{self.show.Title} {self}',
        ]

        self.episodes = [Episode(self, i[1]) for i in episodes.items()]

        self.weights = Weights(
            TITLE = [self.show.Title],
            SEASON = int(self),
            EPISODE = None,
            YEAR = self.show.Year,
            UPLOADED = show.omdb.Released
        )

    @property
    def exists(self) -> bool:
        return all(e.exists for e in self.episodes)
    
    def __format__(self, format_spec:str) -> str:
        return f'{int(self):{format_spec}}'
    
    def __repr__(self) -> str:
        return f'<Season "{self}" - "{self.show.Title}" @{loc(self)}>'

class Episode(MediaItem):

    def __init__(self,
        season: 'Season',
        episode: EpisodeData
    ) -> None:
        
        super().__init__()

        self.show: Show = season.show
        self.season: Season = season
        self.Title: str = episode.Title

        self.dir = season.dir
        """E:/Plex/Media/Shows/{Show}/Season {Season}/"""

        attr(self, '__int__').set(lambda s: episode.Number)

        self.queries = [
            self.show.Title,
            f'{self.show.Title} s{season:02d}e{self:02d}',
            f'{self.show.Title} {season:02d}x{self:02d}',
            f'{self.show.Title} {season}{self:02d}',
            f'{self.show.Title} {season} {self:02d}'
        ]

        self.weights = Weights(
            TITLE = [self.show.Title, self.Title, None],
            YEAR = self.show.Year,
            SEASON = int(self.season),
            EPISODE = int(self),
            UPLOADED = self.show.omdb.Released
        )

    def start(self) -> None:
        self.torrent = self.season.torrent
        super().start()

    @cached_property
    def paths(self) -> tuple[Path, Path]:
        return (
            self.file.path,
            self.dir.child(f'/Season {self.season:02d} Episode {self:02d}.{self.file.path.ext}')
        )
    
    def __format__(self, format_spec:str) -> str:
        return f'{int(self):{format_spec}}'
    
    def __repr__(self) -> str:
        return f'<Episode "{self.season}x{self}" - "{self.show.Title}" @{loc(self)}>'
