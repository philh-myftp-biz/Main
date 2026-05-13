from philh_myftp_biz.web.torrent import TorrentFile, Magnet, NameParser, thePirateBay
from philh_myftp_biz.web.omdb import EpisodeData, Omdb
from philh_myftp_biz.classtools import loc, attr
from philh_myftp_biz.text import similarity
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.db import MimeType
from philh_myftp_biz.pc import Path
from philh_myftp_biz import VERBOSE
from typing import Callable, Any
from . import this

class WEIGHTS(dict[str, Any]):

    def parse(self, name: str):

        parse = NameParser(name)

        logm: str = f'Validating: {name}'

        valid = True

        for key, control in self.items():

            target = getattr(parse, key.lower())

            _valid = getattr(self, key)(
                target = target,
                control = control
            )

            valid &= _valid

            logm += f'\n{key}={_valid:d} | {target=} | {control=}'

        logm += f'\n{valid=}'
 
        Log.VERB(logm)

        return valid

    def TITLE(self,
        target: str, 
        control: str|None
    ) -> bool:
        
        if control is None:
            return True
        else:
            return (similarity(a=target, b=control) > .65)

    def SEASON(self,
        target: int|list[int]|None, 
        control: int
    ) -> bool:
        
        if isinstance(target, int):
            return (control == target)

        elif isinstance(target, list):
            return (control in target)
        
        else:
            return False
        
    def YEAR(self,
        target: int|list[int]|None, 
        control: int|list[int]
    ) -> bool:
        
        if target is None:
            return True
        
        elif isinstance(target, list):
            return (control in target)
        
        else:
        
            if isinstance(control, int):
                MIN = control-1
                MAX = control+1
            else:
                MIN = control[0]-1
                MAX = control[-1]+1

            return (MIN <= target <= MAX)

    def EPISODE(self,
        target: int|list[int]|None, 
        control: int|None
    ) -> bool:
        
        if isinstance(target, list):
            return (control == target[0])
        
        else:
            return (control == target)

class _Template:

    weights: WEIGHTS

    magnet: None|Magnet = None

    queries: list[str]
    """List of queries for the pirate bay"""

    paths: tuple[Path, Path]
    """Get the source and destination paths of the file"""

    finish: Callable[[], None] = lambda s: None
    """tasks to run after the download is complete"""

    dir: Path
    """Parent Folder"""

    def start(self) -> None:
        """Search thepiratebay.org and start the download"""

        magnets = thePirateBay.search(*self.queries)

        magnets.filter(lambda m: self.valid(m.name))

        # Select the most seeded magnet
        self.magnet = magnets.max(func=lambda m: m.seeders)

        # If a magnet has been found
        if self.magnet:

            Log.VERB(
                f'Found: {self=}\n'+ \
                f'{self.magnet.title=}\n'+ \
                f'{self.magnet.seeders=}'
            )

            if not self.magnet.exists:

                # Download the magnet
                self.magnet.start()

                # Stop all files in the magnet
                [f.stop() for f in self.magnet.files]

    @property
    def exists(self) -> bool:
        """Check if the destination file already exists"""

        VERBOSE.pause()

        # Iter through all items in the folder
        for p in self.dir.children:

            # If the file has a valid name
            if self.valid(p):

                VERBOSE.resume()

                return True
            
        VERBOSE.resume()
            
        return False

    def valid(self,
        item: str | Path
    ) -> bool:
        
        if isinstance(item, str):
            return self.weights.parse(item)
        
        else:

            # If the mimetype of the file is 'video' or 'ignore'
            TYPE = (MimeType.Path(item) in ['video', 'ignore'])

            # If the name of the file is valid
            NAME = self.weights.parse(item.name)

            return (TYPE and NAME)
    
    @property
    def file(self) -> TorrentFile | None:
        """File Instance"""
        
        if self.magnet:

            files: list[TorrentFile] = list(filter(
                lambda m: self.valid(m.path),
                self.magnet.files
            ))

            if len(files) > 0:

                return max(
                    files,
                    key = lambda m: m.size
                )

class Movie(_Template):

    dir = this.child('/Media/Movies/')

    def __init__(self,
        title: str,
        year: int,
        todo: Path = None
    ) -> None:
        
        self.Title = title
        self.Year = year

        self.__todo = todo

        self.queries = [
            title,
            f'{title} {year}'
        ]

        self.weights = WEIGHTS()
        self.weights['TITLE'] = self.Title
        self.weights['YEAR'] = self.Year

    @property
    def paths(self):

        # The source file
        src = self.file.path

        # The destination file path
        dst = this.child(f"/Media/Movies/{self.Title} ({self.Year}).{src.ext}")

        return src, dst

    def finish(self):

        # If a todo/placeholder file was passed during initialization
        if self.__todo:

            # Delete the placeholder file
            self.__todo.delete()

    def __repr__(self):
        return f'<Movie "{self.Title} ({self.Year})" @{loc(self)}>'

class Show:

    def __init__(self,
        title: str,
        year: int             
    ) -> None:

        self.Title = title
        self.Year = year

        self.dir = this.child(f"/Media/Shows/{title} ({year})/")
        """../Media/Shows/{Title} ({Year})/"""

        # List of 'Season' OBJs
        self.seasons = [Season(self, *i) for i in Omdb.show(title, year).Seasons.items()]

    def __repr__(self) -> str:
        return f'<Show "{self.Title}" @{loc(self)}>'

class Season(_Template):

    def __init__(self,
        show: 'Show',
        season: str,
        episodes: dict[str, EpisodeData]
    ) -> None:
        
        self.show: Show = show

        attr(self, '__int__').set(lambda s: int(season))

        # Destination File Directory
        self.dir = show.dir.child(f"/Season {self:02d}/")
        """E:/Plex/Media/Shows/{Show}/Season {Season}/"""

        # Create the folder if it doesn't exist
        self.dir.mkdir()

        # List of TPB queries
        self.queries = [
            f'{self.show.Title} Season {self}',
            f'{self.show.Title} s{self:02d}',
            f'{self.show.Title} s{self}',
        ]

        # List of 'Episode' OBJs
        self.episodes = [Episode(self, i[1]) for i in episodes.items()]

        self.weights = WEIGHTS()
        self.weights['TITLE'] = self.show.Title
        self.weights['SEASON'] = int(self)
        self.weights['EPISODE'] = None
        self.weights['YEAR'] = self.show.Year

    @property
    def exists(self) -> bool:
        
        # Iter through all episodes this season
        for episode in self.episodes:

            # If the episode does not exist
            if not episode.exists:
                
                return False
            
        return True
    
    def __format__(self, format_spec:str) -> str:
        return f'{int(self):{format_spec}}'
    
    def __repr__(self) -> str:
        return f'<Season "{self}" - "{self.show.Title}" @{loc(self)}>'

class Episode(_Template):

    def __init__(self,
        season: 'Season',
        episode: EpisodeData
    ) -> None:

        self.show: Show = season.show
        self.season: Season = season
        self.Title: str = episode.Title

        self.dir = season.dir
        """E:/Plex/Media/Shows/{Show}/Season {Season}/"""

        # Integer Function
        attr(self, '__int__').set(lambda s: episode.Number)

        # List of TPB queries
        self.queries = [
            f'{self.show.Title} s{season:02d}e{self:02d}',
            f'{self.show.Title} {season:02d}x{self:02d}',
            f'{self.show.Title} {season}{self:02d}'
        ]

        self.weights = WEIGHTS()
        self.weights['TITLE'] = None
        self.weights['YEAR'] = self.show.Year
        self.weights['SEASON'] = int(self.season)
        self.weights['EPISODE'] = int(self)

    def start(self) -> None:

        self.magnet = self.season.magnet

        # If no file was found in the season magnet
        if self.file is None:

            # Start downloading the episode
            super().start()

    @property
    def paths(self) -> tuple[Path, Path]:

        # The source file
        src = self.file.path
        
        # The destination file path
        dst = self.dir.child(f'/Season {self.season:02d} Episode {self:02d}.{src.ext}')

        return src, dst
    
    def __format__(self, format_spec:str) -> str:
        return f'{int(self):{format_spec}}'
    
    def __repr__(self) -> str:
        return f'<Episode "{self.season}x{self}" - "{self.show.Title}" @{loc(self)}>'

type DOWNLOAD = Movie|Episode
