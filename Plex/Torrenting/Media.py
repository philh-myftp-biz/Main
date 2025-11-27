from __init__ import this, tpb, qbit, driver, omdb, args
from philh_myftp_biz.array import priority, filter, max
from philh_myftp_biz.web import Magnet, api
from philh_myftp_biz.text import similarity
from philh_myftp_biz.pc import Path, mkdir
from philh_myftp_biz.db import MimeType
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

            search = tpb.search(query)

            for m in search:

                seeders = (m.seeders >= args['seeders'])

                quality = (m.quality in args['quality'])

                validName = self.validName(m.title)

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

            # Download the magnet
            self.magnet.start()

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

        # If the mimetype of the file is 'video'
        video = (MimeType.Path(path) == 'video')

        #
        notTODO = (path.ext() != 'todo')

        # If the name of the file is valid
        name = self.validName(path.name())

        return (video and name and notTODO)
    
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
        data = PTN.parse(name)

        # Check if the year is the same
        if 'year' in data:
            year = (data['year'] == self.Year)
        else:
            year = False

        # Check if the file title is more than 60% similar
        if 'title' in data:
            title = similarity(
                a = self.Title, 
                b = data['title']
            ) > .6
        
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

class Season(_Template):

    def __init__(self,
        show: 'Show',
        season: int,
        episodes: list[str]
    ):
        
        self.show = show
        self.season = season

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
        data = PTN.parse(name)

        # Check if the file season is the same
        if 'season' in data:
            season = (data['season'] == int(self.season))
        else:
            season = False

        # Check if the file title is more than 60% similar to the show title
        title = similarity(
            a = data['title'], 
            b = self.show.title
        ) > .6

        return (title and season)

    def __int__(self):
        return self.season
    
    def __format__(self, format_spec):
        return f'{self.season:{format_spec}}'

class Episode(_Template):

    def __init__(self,
        season: 'Season',
        episode: int
    ):
        self.season = season
        self.episode = episode
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
        data = PTN.parse(name)

        # Check if the file season is the same
        if 'season' in data:
            season = (data['season'] == int(self.season))
        else:
            season = False
        
        # Check if the file episode is the same
        if 'episode' in data:
            episode = (data['episode'] == int(self))
        else:
            episode = False

        return (season and episode)

    def paths(self):

        # The source file
        src = self.file.path
        
        # The destination file path
        dst = self.dir.child(f'/Season {self.season:02d} Episode {self:02d}.{src.ext()}')

        return src, dst

    def __int__(self):
        return self.episode
    
    def __format__(self, format_spec):
        return f'{self.episode:{format_spec}}'

    def finish(self):
        pass
