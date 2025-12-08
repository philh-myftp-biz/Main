from philh_myftp_biz.array import List, priority
from philh_myftp_biz.web import Magnet, api
from philh_myftp_biz.text import similarity
from __init__ import this, tpb, omdb, args
from philh_myftp_biz.pc import Path, mkdir
from philh_myftp_biz.db import MimeType
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

        # List of magnets
        magnets: List[Magnet] = List()

        # Iter through the search queries
        for query in self.queries:

            # Iter through all magnets found with the query
            for m in tpb.search(query):

                # If there are at least 5 seeders
                seeders = (m.seeders >= 5)

                # If the name is valid
                name = self.validName(m.title)

                # If the quality is at most 1080p
                quality = m.quality <= 1080

                # Debug: Print magnet details
                if args['verbose']:
                    print('Scanning:', {
                        'name': [name, m.title],
                        'seeders': [seeders, m.seeders],
                        'quality': [quality, m.quality]
                    })

                # If all three conditions are true
                if seeders and name and quality:

                    # Append the magnet to the list
                    magnets += m

        # Return the best remaining magnet
        self.magnet = magnets.max(
            lambda m: priority(
                _1 = m.quality, # 1st. Quality
                _2 = m.seeders, # 2nd. Seeders
                reverse = True
            ) 
        )

        # If a magnet has been found
        if self.magnet:

            # Debug: Print magnet details
            if args['verbose']:
                print('Found:', {
                    'name': self.magnet.title,
                    'seeders': self.magnet.seeders,
                    'quality': self.magnet.quality
                })

            # Download the magnet
            self.magnet.start()

        # If a magnet has not been found and debug
        elif args['verbose']:

            # Debug: Print magnet details
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
        """Movie Title"""

        self.Year = year
        """Release Year"""
        
        self.__todo = todo
        """Placeholder File"""

        self.queries = [
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

                    # Start downloading the file
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

        # Stop the magnet
        self.magnet.stop()

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
        """Show Title"""

        self.year = year
        """Release Year"""

        self.dir = this.dir.child(f"/Media/Shows/{title} ({year})/")
        """../Media/Shows/{Title} ({Year})/"""

        #
        show = omdb.show(title, year)

        self.__seasons: list[str] = []
        """raw list of seasons"""

        # Fetch show details from the Open Movie Database
        if show:
            self.__seasons = show.Seasons

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
        """This Show"""

        self._season = season
        """season #"""

        self.dir = show.dir.child(f"/Season {self:02d}/")
        """../Season {Season}/"""

        # Create the folder if it doesn't exist
        if not self.dir.exists():
            mkdir(self.dir)

        self.queries = [
            f'{self.show.title} {self.show.year} Season {season:02d}',
            f'{self.show.title} Season {season:02d}',
            f'{self.show.title} s{season:02d}',
        ]

        self.episodes: list[Episode] = []
        """List of Episodes"""

        # Iter through all raw episodes
        for e in episodes:

            # Append an episode object to the list
            self.episodes += [Episode(
                season = self, # This Season
                episode = int(e) # Episode number
            )]

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

        # Parse the file name
        data: Dict[str] = Dict(PTN.parse(name))

        # Check if the file season is the same
        season = (data['season'] == int(self))

        # Check if the title is more than 60% similar to the show title
        title = (similarity(data['title'], self.show.title) > .6)

        return (title and season)

    def __int__(self):
        return self._season
    
    def __format__(self, format_spec):
        return f'{self._season:{format_spec}}'
    
    def __str__(self):
        from philh_myftp_biz.classOBJ import location

        return f'<Season "{self}" @{location(self)}>'

class Episode(_Template):

    def __init__(self,
        season: 'Season',
        episode: int
    ):

        self.season = season
        """This Season"""

        self.show = season.show
        """This Show"""

        self._episode = episode
        """Episode #"""
        
        self.dir = season.dir

        self.queries = [
            f'{self.show.title} s{season:02d}e{self:02d}',
            f'{self.show.title} {season:02d}x{self:02d}'
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

        #
        if self.file:

            #
            self.file.start()

    def validName(self, name:str) -> bool:

        # Parse the file name
        data: Dict[str] = Dict(PTN.parse(name))

        # Check if the file season is the same
        season = (data['season'] == int(self.season))

        # If the name has multiple episode #s
        if isinstance(data['episode'], list):
            # If the 1st num is the same
            episode = (int(self) == data['episode'][0])
        
        else:
            # If the episode num is the same
            episode = (int(self) == data['episode'])

        return (season and episode)

    def paths(self):

        # The source file
        src = self.file.path
        
        # The destination file path
        dst = self.dir.child(f'/Season {self.season:02d} Episode {self:02d}.{src.ext()}')

        return src, dst

    def __int__(self):
        return self._episode
    
    def __format__(self, format_spec):
        return f'{self._episode:{format_spec}}'

    def finish(self):

        # Stop downloading the file
        self.file.stop()
