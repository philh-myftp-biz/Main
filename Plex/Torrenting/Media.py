from philh_myftp_biz.text import similarity
from philh_myftp_biz.web import Magnet, api
from __init__ import this, tpb, omdb, args
from philh_myftp_biz.pc import Path, mkdir
from philh_myftp_biz.classOBJ import loc
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.db import MimeType
from philh_myftp_biz.array import List
from philh_myftp_biz.json import Dict
from typing import Callable
import PTN

class PARAMS:
    
    def TITLE(
        target: str, 
        control: str
    ):
        return (similarity(target, control) > .65)

    def SEASON(
        target: int|list[int], 
        control: int
    ):
        if isinstance(target, int):
            return (control == target)

        elif isinstance(target, list):
            return (control in target)
        
        else:
            return False
        
    def YEAR(
        target: int|None, 
        control: int|list[int]
    ):
        if target is None:
            return True
        
        else:
        
            if isinstance(control, int):
                control = [control]

            for c in control:

                if abs(c - target) < 2:
                    return True
                
            return False
        
    def EPISODE(
        target: int|list[int]|None, 
        control: int|None
    ):
        if isinstance(target, list):
            return (control in target)
        
        else:
            return (control == target)

class _Template:

    validName: Callable[[str], bool]
    """
    Check if a string has valid filename syntax
    """

    magnet: Magnet = None
    """
    Magnet Instance
    """

    file: api.qBitTorrent.File = None
    """
    File Instance
    """

    queries: list[str]
    """
    List of queries to be used when searching thepiratebay.org 
    """

    paths: Callable[[], tuple[Path, Path]]
    """
    Get the source and destination paths of the file
    """

    finish: Callable[[], None] = lambda s: None
    """
    Object-Specific tasks to run after the download is complete
    """

    dir: Path
    """
    Parent Folder
    """

    def start(self):
        """
        Search thepiratebay.org and start the download
        """

        # List of magnets
        magnets: List[Magnet] = List()

        # Iter through the search queries
        for query in self.queries:

            # Iter through all magnets found with the query
            for m in tpb.search(query):

                # If the title is valid
                TITLE = self.validName(m.title)
                SEEDERS = (m.seeders > 0)

                Log.VERB(
f"""Validating: {m=}
{  TITLE=:d} | in={m.title=}
{SEEDERS=:d} | in={m.seeders}"""
                )

                if TITLE and SEEDERS:
                    # Append the magnet to the list
                    magnets += m

        # Select the most seeded magnet
        self.magnet = magnets.max(lambda m: m.seeders)

        # If a magnet has been found
        if self.magnet:

            Log.VERB(
                f'Found: {self=}\n'+ \
                f'{self.magnet.title=}\n'+ \
                f'{self.magnet.seeders=}'
            )

            # 
            if not self.magnet.exists():

                # Download the magnet
                self.magnet.start()

                # Stop all files in the magnet
                for file in self.magnet.files():
                    file.stop()

        # If a magnet has not been found
        else:

            # Log magnet details
            Log.WARN(f'None Found: {self=}')

    def exists(self) -> bool:
        """
        Check if the destination file already exists
        """

        # Iter through all items in the folder
        for p in self.dir.children():

            # If the file has a valid name
            if self.validFile(p):

                return True
            
        return False

    def validFile(self, path:Path):
        """
        Check a file for the following conditions:
            - File is a video
            - File does not end with '.todo'
            - Name is valid
        """

        # If the mimetype of the file is 'video' or 'ignore'
        TYPE = (MimeType.Path(path) in ['video', 'ignore'])

        # If the name of the file is valid
        NAME = self.validName(path.name())

        return (TYPE and NAME)
    
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

    def start(self):

        # Start the download
        super().start()

        # If a magnet was found
        if self.magnet:
            
            # Iter through all files in the magnet
            for f in self.magnet.files():
                
                # Check if the file is valid
                if self.validFile(f.path):
                    
                    # Set the 'file' attr to the current file
                    self.file = f
                    
                    break

    def validName(self, name:str) -> bool:
        
        # Parse the given name
        data: Dict[str] = Dict(PTN.parse(name))

        TITLE = PARAMS.TITLE(
            target = data['title'],
            control = self.Title
        )

        # Check if the year is either the same or missing
        YEAR = PARAMS.YEAR(
            target = data['year'],
            control = self.Year
        )

        Log.VERB(
f"""Validating: {name=}
{TITLE=:d} | in={data['title']} | own={self.Title}
{ YEAR=:d} | in={data['year']} | own={self.Year}"""
        )
        
        return TITLE and YEAR

    def paths(self):

        # The source file
        src = self.file.path

        # The destination file path
        dst = this.child(f"/Media/Movies/{self.Title} ({self.Year}).{src.ext()}")

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
    ):

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
        episodes: dict[str, api.omdb.Episode]
    ):
        
        # Store 'Show' OBJ
        self.show = show

        # Integer Function
        self.__int = int(season)

        # Destination File Directory
        self.dir = show.dir.child(f"/Season {self:02d}/")
        """../Season {Season}/"""

        self.Years = [
            show.Year, 
            (show.Year + int(self))
        ]

        # Create the folder if it doesn't exist
        mkdir(self.dir)

        # List of TPB queries
        self.queries = [
            f'{self.show.Title} {self.Years[0]} Season {self:02d}',
            f'{self.show.Title} Season {self:02d}',
            f'{self.show.Title} s{self:02d}',
        ]

        # List of 'Episode' OBJs
        self.episodes = [Episode(self, i[1]) for i in episodes.items()]

    def start(self):

        # Start the download
        super().start()

        # If a magnet has been found
        if self.magnet:

            # Iter through all downloading files
            for f in self.magnet.files():

                # Pause the file download
                f.stop()

    def exists(self):
        
        # Iter through all episodes this season
        for episode in self.episodes:

            # If the episode does not exist
            if not episode.exists():
                
                return False
            
        return True

    def validName(self, name:str) -> bool:

        # Parse the given name
        data: Dict[str] = Dict(PTN.parse(name))

        TITLE = PARAMS.TITLE(
            target = data['title'],
            control = self.show.Title
        )

        SEASON = PARAMS.SEASON(
            target = data['season'],
            control = int(self)
        )

        EPISODE = PARAMS.EPISODE(
            target = data['episode'],
            control = None
        )

        # Check if the year is either the same or missing
        YEAR = PARAMS.YEAR(
            target = data['year'],
            control = self.Years
        )

        Log.VERB(
f"""Validating: {name=}
{  TITLE=:d} | in={data['title']} | own={self.show.Title}
{ SEASON=:d} | in={data['season']} | own={int(self)}
{EPISODE=:d} | in={data['episode']}
{   YEAR=:d} | in={data['year']} | own={self.Years}"""
        )

        return all([TITLE, SEASON, EPISODE, YEAR])
    
    def __int__(self):
        return self.__int

    def __format__(self, format_spec):
        return f'{int(self):{format_spec}}'
    
    def __repr__(self):
        return f'<Season "{self}" - "{self.show.Title}" @{loc(self)}>'

class Episode(_Template):

    def __init__(self,
        season: 'Season',
        episode: api.omdb.Episode
    ):

        # Store 'Show' OBJ
        self.show = season.show
        
        # Store 'Season' OBJ
        self.season = season

        # Store Episode Title
        self.Title = episode.Title

        # Store Directory
        self.dir = season.dir
        """../Season {Season}/"""

        # Integer Function
        self.__int = episode.Number

        # List of TPB queries
        self.queries = [
            f'{self.show.Title} s{season:02d}e{self:02d}',
            f'{self.show.Title} {season:02d}x{self:02d}',
            f'{self.show.Title} {self.Title}'
        ]

    def start(self):

        # If this season is downloading as one magnet
        if self.season.magnet:

            # Iter through all files in the season download
            for file in self.season.magnet.files():

                # If the file is valid
                if self.validFile(file.path):

                    # Set this objects 'file' attr to the file
                    self.file = file

                    # Set this objects 'magnet' attr to the season magnet
                    self.magnet = self.season.magnet

                    break

        # If no file was found
        if self.file is None:

            # Start downloading the episode
            super().start()

            # If a magnet has been found
            if self.magnet:

                # Iter through all files in the magnet
                for file in self.magnet.files():

                    # If the file is valid
                    if self.validFile(file.path):

                        # Set this objects 'file' attr to the file
                        self.file = file

                        break

    def validName(self, name:str) -> bool:

        # Parse the given name
        data: Dict[str] = Dict(PTN.parse(name))

        TITLE = PARAMS.TITLE(
            target = data['title'],
            control = self.show.Title
        )

        SEASON = PARAMS.SEASON(
            target = data['season'],
            control = int(self.season)
        )

        EPISODE = PARAMS.EPISODE(
            target = data['episode'],
            control = int(self)
        )

        # Check if the year is either the same or missing
        YEAR = PARAMS.YEAR(
            target = data['year'],
            control = self.season.Years
        )

        Log.VERB(
f"""Validating: {name=}
{  TITLE=:d} | in={data['title']} | own={self.show.Title}
{ SEASON=:d} | in={data['season']} | own={int(self.season)}
{EPISODE=:d} | in={data['episode']} | own={int(self)}
{   YEAR=:d} | in={data['year']} | own={self.show.Year}"""
        )

        return all([TITLE, SEASON, EPISODE, YEAR])

    def paths(self):

        # The source file
        src = self.file.path
        
        # The destination file path
        dst = self.dir.child(f'/Season {self.season:02d} Episode {self:02d}.{src.ext()}')

        return src, dst
    
    def __int__(self):
        return self.__int

    def __format__(self, format_spec):
        return f'{int(self):{format_spec}}'
    
    def __repr__(self):
        return f'<Episode "{self.season}x{self}" - "{self.show.Title}" @{loc(self)}>'
