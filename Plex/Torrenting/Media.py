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

                # If there are enough seeders
                SEEDERS = (m.seeders >= args['seeders'])

                Log.VERB(f'Scanning: {args['seeders']=} {SEEDERS=} | {m.title=} {TITLE=}')

                if TITLE and SEEDERS:
                    # Append the magnet to the list
                    magnets += m

        # Find the best remaining magnet
        self.magnet = magnets.max(
            lambda m: m.seeders
        )

        # If a magnet has been found
        if self.magnet:

            Log.INFO(f'Found: {self.magnet.title=} | {self.magnet.seeders=}')

            # Download the magnet
            self.magnet.start()

            # Stop all files in the magnet
            for file in self.magnet.files():
                file.stop()

        # If a magnet has not been found and debug
        elif args['verbose']:

            # Log magnet details
            Log.INFO('Found: None')

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
        type = (MimeType.Path(path) in ['video', 'ignore'])

        # If the name of the file is valid
        name = self.validName(path.name())

        return (type and name)
    
class Movie(_Template):

    dir = this.dir.child('/Media/Movies/')

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

        # If the title is similar enough
        TITLE = (similarity(self.Title, data['title']) > args['similarity'])

        # If the year is the same
        YEAR = (data['year'] == self.Year)

        Log.VERB(f'Validating: {name=} | {data['title']=} {self.Title=} {TITLE=} | {data['year']=} {self.Year=} {YEAR=}')
        
        return (TITLE and YEAR)

    def paths(self):

        # The source file
        src = self.file.path

        # The destination file path
        dst = this.dir.child(f"/Media/Movies/{self.Title} ({self.Year}).{src.ext()}")

        return src, dst

    def finish(self):

        # If a todo/placeholder file was passed during initialization
        if self.__todo:

            # Delete the placeholder file
            self.__todo.delete()

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
        self.dir = this.dir.child(f"/Media/Shows/{title} ({year})/")
        """../Media/Shows/{Title} ({Year})/"""

        # List of 'Season' OBJs
        self.seasons = [Season(self, *i) for i in omdb.show(title, year).Seasons.items()]

    def __str__(self):
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

        # Create the folder if it doesn't exist
        mkdir(self.dir)

        # List of TPB queries
        self.queries = [
            f'{self.show.Title} {self.show.Year} Season {self:02d}',
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

        # If the title is similar
        TITLE = (similarity(data['title'], self.show.Title) > args['similarity'])

        # If the file season is the same
        SEASON = (data['season'] == int(self))

        # If no episode # is found
        EPISODE = (data['episode'] is None)

        # Check if the year is either the same or missing
        YEAR = ((data['year'] is None) or (data['year'] == self.show.Year))

        Log.VERB(f'Validating: {name=} | {data['title']=} {self.show.Title=} {TITLE=} | {data['season']=} {int(self)=} {SEASON=} | {data['episode']=} {EPISODE=} | {data['year']=} {self.show.Year=} {YEAR=}')

        return (TITLE and SEASON and EPISODE and YEAR)
    
    def __int__(self):
        return self.__int

    def __format__(self, format_spec):
        return f'{int(self):{format_spec}}'
    
    def __str__(self):
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

        # If the title is either similar or missing
        TITLE = (data['title'] is None) or (similarity(data['title'], self.show.Title) > args['similarity'])

        # If the season is the same
        SEASON = (data['season'] == int(self.season))

        # If the name has multiple episode #s
        if isinstance(data['episode'], list):
            # If the 1st num is the same
            EPISODE = (int(self) == data['episode'][0])
        else:
            # If the episode num is the same
            EPISODE = (int(self) == data['episode'])

        # Check if the year is either the same or missing
        YEAR = ((data['year'] is None) or (data['year'] == self.show.Year))

        Log.VERB(f'Validating: {name=} | {data['title']=} {self.show.Title=} {TITLE=} | {data['season']=} {int(self.season)=} {SEASON=} | {data['episode']=} {int(self)=} {EPISODE=} | {data['year']=} {self.show.Year=} {YEAR=}')

        return (TITLE and SEASON and EPISODE and YEAR)

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
    
    def __str__(self):
        return f'<Episode "{self.season}x{self}" - "{self.show.Title}" @{loc(self)}>'
