from philh_myftp_biz.array import priority, max
from philh_myftp_biz.web import Magnet, api
from philh_myftp_biz.text import similarity
from __init__ import this, tpb, omdb, args
from philh_myftp_biz.pc import Path, mkdir
from philh_myftp_biz.db import MimeType
from typing import Callable
import PTN
from philh_myftp_biz.json import Dict
from philh_myftp_biz.file import YAML

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

    paths: Callable[[], list[Path, Path]]
    """
    Get the source and destination paths of the file
    """

    finish: Callable[[], None]
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

        magnets: list[Magnet] = []

        for query in self.queries:

            for m in tpb.search(query):

                seeders = (m.seeders >= args['seeders'])

                quality = (m.quality in args['quality'])

                validName = self.validName(m.title)

                if args['verbose']:
                    print('Scanning:', {
                        'name': [validName, m.title],
                        'seeders': [seeders, m.seeders],
                        'quality': [quality, m.quality]
                    })

                if seeders and quality and validName:

                    magnets += [m]

        # Return the best remaining magnet
        self.magnet = max(
            array = magnets,
            func = lambda m: priority(
                _1 = m.quality,
                _2 = m.seeders,
                reverse = True
            ) 
        )

        # If a magnet has been found
        if self.magnet:

            if args['verbose']:
                print('Found:', {
                    'name': self.magnet.title,
                    'seeders': self.magnet.seeders,
                    'quality': self.magnet.quality
                })

            # Download the magnet
            self.magnet.start()

        elif args['verbose']:

            print('Found:', None)

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
        self.Year = year
        self.__todo = todo

        self.queries = [
            f'{title} {year}'
        ]
       
    def start(self):

        super().start()

        # If a magnet was found
        if self.magnet:
            
            # Iter through all files in the magnet
            for f in self.magnet.files():
                
                # Check if the file is valid
                if self.validFile(f.path):
                    
                    # Set the 'file' attr to the current file
                    self.file = f

                    #
                    f.start(True)
                    
                    break

    def validName(self, name:str) -> bool:
        
        # Parse the file name
        data: Dict[str] = Dict(PTN.parse(name))

        # Check if the year is the same
        year = (data['year'] == self.Year)

        # Check if the title is more than 60% similar
        title = (similarity(self.Title, data['title']) > .6)
        
        return (year and title)

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

        self.title = title
        self.year = year

        self.dir = this.dir.child(f"/Media/Shows/{title} ({year})/")
        """../Media/Shows/{Title} ({Year})/"""

        self.config = Dict(YAML(self.dir.child('config.yaml')))
        """Show Configuration"""

        # Set the default 'quality' config value
        if self.config['quality'] is None:
            self.config['quality'] = [720, 1080]

        # Fetch show details from the Open Movie Database
        self.__seasons = omdb.show(title, year).Seasons

    def Seasons(self):

        # Iter through all seasons from the omdb data
        for s in self.__seasons:
            
            # Yield a Season Instance 
            yield Season(
                show = self, # This Show
                season = int(s), # Season number
                episodes = self.__seasons[s] # Array of episode numbers as strings
            )

    def __str__(self):
        from philh_myftp_biz.classOBJ import location
        from philh_myftp_biz.text import abbreviate

        return f'<Show "{abbreviate(15, self.title)}" @{location(self)}>'

class Season(_Template):

    def __init__(self,
        show: 'Show',
        season: int,
        episodes: list[str]
    ):
        
        self.show = show
        self.__int = season

        self._started: bool = False

        self.dir = show.dir.child(f"/Season {self:02d}/")
        """../Season {Season}/"""

        if not self.dir.exists():
            mkdir(self.dir)

        self.queries = [
            f'{self.show.title} {self.show.year} Season {season:02d}',
            f'{self.show.title} Season {season:02d}',
            f'{self.show.title} s{season:02d}',
        ]

        self.episodes: list[Episode] = []

        for e in episodes:
            self.episodes += [Episode(
                season = self, # This Season
                episode = int(e) # Episode number
            )]

    def start(self):

        super().start()

        if self.magnet:

            for f in self.magnet.files():
                f.stop()

    def exists(self):
        for episode in self.episodes:
            if not episode.exists():
                return False
        return True

    def validName(self, name:str) -> bool:

        # Parse the file name
        data: Dict[str] = Dict(PTN.parse(name))

        # Check if the file season is the same
        season = (data['season'] == int(self))

        # Check if the title is more than 60% similar to the show title
        title = (similarity(data['title'], self.show.title) > .6)

        return (title and season)

    def __int__(self):
        return self.__int
    
    def __format__(self, format_spec):
        return f'{self.__int:{format_spec}}'
    
    def __str__(self):
        from philh_myftp_biz.classOBJ import location

        return f'<Season "{self}" @{location(self)}>'

class Episode(_Template):

    def __init__(self,
        season: 'Season',
        episode: int
    ):

        self.season = season
        self.__int = episode
        self.show = season.show
        self.dir = season.dir

        self.queries = [
            f'{self.show.title} s{season:02d}e{self:02d}',
            f'{self.show.title} {season:02d}x{self:02d}'
        ]

    def start(self):

        if self.season.magnet:

            for file in self.season.magnet.files():

                if self.validFile(file.path):

                    file.start()

                    self.file = file
                    self.magnet = self.season.magnet

        if self.file is None:
            super().start()

    def validName(self, name:str) -> bool:

        # Parse the file name
        data: Dict[str] = Dict(PTN.parse(name))

        # Check if the file season is the same
        season = (data['season'] == int(self.season))

        if isinstance(data['episode'], list):
            episode = (int(self) == data['episode'][0])
        else:
            episode = (int(self) == data['episode'])

        return (season and episode)

    def paths(self):

        # The source file
        src = self.file.path
        
        # The destination file path
        dst = self.dir.child(f'/Season {self.season:02d} Episode {self:02d}.{src.ext()}')

        return src, dst

    def __int__(self):
        return self.__int
    
    def __format__(self, format_spec):
        return f'{self.__int:{format_spec}}'

    def finish(self):
        pass
