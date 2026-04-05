from philh_myftp_biz.web.torrent import TorrentFile, Magnet
from philh_myftp_biz.web.omdb import EpisodeData
from philh_myftp_biz.text import similarity
from philh_myftp_biz.classtools import loc
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.db import MimeType
from philh_myftp_biz.json import Dict
from typing import Callable, Literal
from philh_myftp_biz.pc import Path
from philh_myftp_biz import VERBOSE
from . import this, tpb, omdb
from functools import cache
import PTN

class WEIGHTS:

    data: list[dict[Literal['name', 'valid', 'target', 'control'], str]]

    def __init__(self, name:str):

        self.data = []

        self.name: str = name

    @property
    def valid(self) -> bool:
        
        outp: str = f'Validating: {self.name}'

        for item in self.data:

            outp += f'\n{item['name']}={item['valid']:d} | target={item['target']} | control={item['control']}'
        
        Log.VERB(outp)

        return all(i['valid'] for i in self.data)
    
    def TITLE(self,
        target: str, 
        control: str|None
    ) -> None:
        
        if control is None:
            valid = True
        else:
            valid = (similarity(a=target, b=control) > .65)

        self.data += [{
            'name': 'TITLE',
            'valid': valid,
            'target': target,
            'control': control
        }]

    def SEASON(self,
        target: int|list[int]|None, 
        control: int
    ) -> None:
        
        if isinstance(target, int):
            valid = (control == target)

        elif isinstance(target, list):
            valid = (control in target)
        
        else:
            valid = False
        
        self.data += [{
            'name': 'SEASON',
            'valid': valid,
            'target': target,
            'control': control
        }]
        
    def YEAR(self,
        target: int|list[int]|None, 
        control: int|list[int]
    ):
        if target is None:
            valid = True
        
        elif isinstance(target, list):
            valid = (control in target)
        
        else:
        
            if isinstance(control, int):
                MIN = control-1
                MAX = control+1
            else:
                MIN = control[0]-1
                MAX = control[-1]+1

            valid = (MIN <= target <= MAX)

        self.data += [{
            'name': 'YEAR',
            'valid': valid,
            'target': target,
            'control': control
        }] 

    def EPISODE(self,
        target: int|list[int]|None, 
        control: int|None
    ) -> None:
        if isinstance(target, list):
            valid = (control in target)
        
        else:
            valid = (control == target)

        self.data += [{
            'name': 'EPISODE',
            'valid': valid,
            'target': target,
            'control': control
        }]

class _Template:

    validName: Callable[[str], bool]
    """Check if a string has valid filename syntax"""

    magnet: None|Magnet = None
    """Magnet Instance"""

    queries: list[str]
    """List of queries for the pirate bay"""

    paths: tuple[Path, Path]
    """Get the source and destination paths of the file"""

    finish: Callable[[], None] = lambda s: None
    """tasks to run after the download is complete"""

    dir: Path
    """Parent Folder"""

    _int: int

    def start(self) -> None:
        """Search thepiratebay.org and start the download"""

        magnets = List(tpb.search(*self.queries))

        magnets.filter(lambda m: self.validName(m.title))

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
            if self.validFile(path=p):

                VERBOSE.resume()

                return True
            
        VERBOSE.resume()
            
        return False

    def validFile(self, path:Path) -> bool:
        """
        Check a file for the following conditions:
            - File is a video
            - File does not end with '.todo'
            - Name is valid
        """

        # If the mimetype of the file is 'video' or 'ignore'
        TYPE = (MimeType.Path(path) in ['video', 'ignore'])

        # If the name of the file is valid
        NAME = self.validName(path.name)

        return (TYPE and NAME)
    
    @property
    def file(self) -> TorrentFile | None:
        """File Instance"""
        
        if self.magnet:

            files: list[TorrentFile] = list(filter(
                lambda m: self.validFile(m.path),
                self.magnet.files
            ))

            if len(files) > 0:

                return max(
                    files,
                    key = lambda m: m.size
                )

    def __int__(self) -> int:
        return self._int

class Movie(_Template):

    dir = this.child('/Media/Movies/')

    def __init__(self,
        title: str,
        year: int,
        todo: Path = None
    ):
        
        self.Title = title
        """Movie Title"""

        self.Year = year
        """Release Year"""
        
        self.__todo = todo
        """Placeholder File"""

        self.queries = [
            title,
            f'{title} {year}'
        ]

    @cache
    def validName(self, name:str) -> bool:
        
        # Parse the given name
        data: Dict[str] = Dict(PTN.parse(name))

        params = WEIGHTS(name)

        params.TITLE(
            target = data['title'],
            control = self.Title
        )

        # Check if the year is either the same or missing
        params.YEAR(
            target = data['year'],
            control = self.Year
        )
        
        return params.valid

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

        # Store title
        self.Title = title
        
        # Store year 
        self.Year = year

        # Show Root Directory
        self.dir = this.child(f"/Media/Shows/{title} ({year})/")
        """../Media/Shows/{Title} ({Year})/"""

        # List of 'Season' OBJs
        self.seasons = [Season(self, *i) for i in omdb.show(title, year).Seasons.items()]

    def __repr__(self):
        return f'<Show "{self.Title}" @{loc(self)}>'

class Season(_Template):

    def __init__(self,
        show: 'Show',
        season: str,
        episodes: dict[str, EpisodeData]
    ) -> None:
        
        # Store 'Show' OBJ
        self.show: Show = show

        # Integer Function
        self._int = int(season)

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

    @property
    def exists(self) -> bool:
        
        # Iter through all episodes this season
        for episode in self.episodes:

            # If the episode does not exist
            if not episode.exists:
                
                return False
            
        return True

    @cache
    def validName(self, name:str) -> bool:

        # Parse the given name
        data: Dict[str] = Dict(PTN.parse(name))

        params = WEIGHTS(name)

        params.TITLE(
            target = data['title'],
            control = self.show.Title
        )

        params.SEASON(
            target = data['season'],
            control = int(self)
        )

        params.EPISODE(
            target = data['episode'],
            control = None
        )

        params.YEAR(
            target = data['year'],
            control = self.show.Year
        )

        return params.valid
    
    def __format__(self, format_spec:str) -> str:
        return f'{int(self):{format_spec}}'
    
    def __repr__(self) -> str:
        return f'<Season "{self}" - "{self.show.Title}" @{loc(self)}>'

class Episode(_Template):

    def __init__(self,
        season: 'Season',
        episode: EpisodeData
    ) -> None:

        # Store 'Show' OBJ
        self.show: Show = season.show
        
        # Store 'Season' OBJ
        self.season: Season = season

        # Store Episode Title
        self.Title: str = episode.Title

        # Store Directory
        self.dir = season.dir
        """E:/Plex/Media/Shows/{Show}/Season {Season}/"""

        # Integer Function
        self._int = episode.Number

        # List of TPB queries
        self.queries = [
            f'{self.show.Title} s{season:02d}e{self:02d}',
            f'{self.show.Title} {season:02d}x{self:02d}',
            f'{self.show.Title} {season}{self:02d}'
        ]

    def start(self) -> None:

        self.magnet = self.season.magnet

        # If no file was found in the season magnet
        if self.file is None:

            # Start downloading the episode
            super().start()

    @cache
    def validName(self, name:str) -> bool:

        # Parse the given name
        data: Dict[str] = Dict(PTN.parse(name))

        params = WEIGHTS(name)

        params.TITLE(
            target = data['title'],
            control = None
        )

        params.SEASON(
            target = data['season'],
            control = int(self.season)
        )

        params.EPISODE(
            target = data['episode'],
            control = int(self)
        )

        params.YEAR(
            target = data['year'],
            control = self.show.Year
        )

        return params.valid

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
