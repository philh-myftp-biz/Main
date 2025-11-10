from philh_myftp_biz.array import priority, filter, max
from Instances import this, tpb, qbit, driver, omdb
from philh_myftp_biz.web import Magnet, api
from philh_myftp_biz.db import MimeType
from philh_myftp_biz.pc import Path
from difflib import SequenceMatcher
from typing import Callable
import RTN, PTN

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

        # Create new ThePirateBay search
        search = tpb.search(
            *self.queries,
            driver = driver,
            qbit = qbit
        )

        # Remove magnets with less than 15 seeders
        magnets = filter(
            array = list(search),
            func = lambda m: (m.seeders >= 15)
        )

        # Remove magnets that aren't 720p or 1080p
        magnets = filter(
            array = magnets,
            func = lambda m: (m.quality in [720, 1080] )
        )

        # Remove magnets without a valid name
        magnets = filter(
            array = magnets,
            func = lambda m: self.validName(m.title)
        )

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

    def validFile(self, path:Path):
        """
        Check a file for the following conditions:
            - File is a video
            - Name is valid
        """

        # If the mimetype of the file is 'video'
        video = (MimeType.Path(path) == 'video')

        # If the name of the file is valid
        name = self.validName(path.name())

        return (video and name)
    
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

        self.start()

        # If a magnet was found
        if self.magnet:
            
            # Iter through all files in the magnet
            for f in self.magnet.files():
                
                # If the file is valid
                if self.validFile(f.path):
                    
                    # Set the 'file' attr to the current file
                    self.file = f
                    
                else:

                    # Prevent the file from downloading
                    f.stop()

    def validName(self, name:str) -> bool:
        
        # Parse the file name
        data = RTN.parse(name)

        # Check if the year is the same
        year = (data.year == self.Year)

        # Check if the file title is more than 60% similar
        title = SequenceMatcher(None,
            a = self.Title, 
            b = data.parsed_title
        ).ratio() > .6
        
        return (year and title)

    def paths(self):

        # The source file
        src = self.file.path

        # The destination file path
        dst = this.dir.child(f"/Movies/['{self.Title}', {self.Year}].{src.ext()}")

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

        self.dir = show.dir.child(f"/Season {self}/")
        """../Season {Season}/"""

        self.queries = [
            f'{self.show.title} {self.show.year} Season {season}',
            f'{self.show.title} Season {season}',
            f'{self.show.title} s{season}',
        ]

        # List of episodes
        self.episodes: list[Episode] = []

        # Iter through stringified episode numbers
        for e in episodes:

            # Append an Episode Instance to the list
            self.episodes += [Episode(
                season = self, # This Season
                episode = int(e) # Episode number
            )]
  
        super().start()

        # If a magnet was found
        if self.magnet:

            # Iter through all files in the magnet
            for f in self.magnet.files():

                # Iter through all episodes in this season
                for e in self.episodes:

                    # Check if the file is valid for the episode
                    if e.validFile(f.path):

                        # Set attrs on the episode
                        e.magnet = self.magnet
                        e.file = f

        # If a magnet was not found
        else:

            # Iter through all files in the magnet
            for e in self.episodes:

                # If the episode file does not already exist
                if not e.exists():

                    # Start downloading the episode
                    e.start()

    def validName(self, name:str) -> bool:

        # Parse the file name
        data = PTN.parse(name)

        # Check if the file season is the same
        if 'season' in data:
            season = (data['season'] == int(self.season))
        else:
            season = False

        # Check if the file title is more than 60% similar to the show title
        title = SequenceMatcher(None,
            a = data['title'], 
            b = self.show.title
        ).ratio() > .6

        return (title and season)

    def __int__(self):
        return self.season

    def __str__(self):
        return str(self.season).zfill(2)

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
            f'{self.show.title} s{season}e{self}',
            f'{self.show.title} {season}x{self}'
        ]

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
        dst = self.dir.child(f'/Season {self.season} Episode {self}.{src.ext()}')

        return src, dst

    def __int__(self):
        return self.episode
    
    def __str__(self):
        return str(self.episode).zfill(2)

    def finish(self):
        pass

Downloadable = list[Movie | Episode | Season]