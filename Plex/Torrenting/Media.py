from philh_myftp_biz.array import priority, filter, max
from Instances import this, tpb, qbit, driver, omdb
from philh_myftp_biz.web import Magnet, api
from philh_myftp_biz.pc import Path
from philh_myftp_biz.classOBJ import log
from difflib import SequenceMatcher
from typing import Generator, Callable
from philh_myftp_biz.db import MimeType
import RTN, PTN

def max_magnet(
    media: 'Episode | Movie | Season',
    magnets: list[Magnet]
) -> None | Magnet:

    # Remove magnets with less than 15 seeders
    magnets = filter(
        array = magnets,
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
        func = lambda m: media.validName(m.title)
    )

    # Return the best remaining magnet
    return max(
        array = magnets,
        func = lambda m: priority(
            _1 = m.quality,
            _2 = m.seeders,
            reverse = True
        ) 
    )

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
    Magnet Instance
    """

    queries: list[str]
    """ """

    paths: Callable[[], list[Path, Path]]
    """
    
    """

    dir: Path
    """
    Parent Folder
    """

    def finish(self) -> None:
        """
        Object-Specific tasks to run after download is complete
        """

    def finished(self):

        for f in self.files():
            
            if not f.finished():
                return False
            
        return True

    def start(self):
        """
        
        """

        # Create new ThePirateBay search
        search = tpb.search(
            *self.queries,
            driver = driver,
            qbit = qbit
        )

        #
        self.magnet = max_magnet(
            media = self,
            magnets = list(search)
        )

        if self.magnet:
            self.magnet.start()

    def exists(self) -> bool:
        """

        """

        for p in self.dir.children():

            if self.validName(p.name()):

                return True

    def validFile(self, path:Path):

        video = (MimeType.Path(path) == 'video')

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

        if self.magnet:
            
            for f in self.magnet.files():
                
                if self.validFile(f.path):
                    
                    self.file = f
                    
                    break

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
        
        #
        return (year and title)

    def DST(self, src:Path):
        return this.dir.child(f"/Movies/['{self.Title}', {self.Year}].{src.ext()}")

    def finish(self):
        #
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

        for s in self.__seasons:
            
            yield Season(
                show = self,
                season = int(s),
                episodes = self.__seasons[s]
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

        self.episodes: list[Episode] = []

        for e in episodes:
            self.episodes += [Episode(
                season = self,
                episode = int(e)
            )]
  
        super().start()

        if self.magnet:

            for f in self.magnet.files():

                for e in self.episodes:

                    if e.validFile(f.path):

                        e.magnet = self.magnet
                        e.file = f

        else:

            for e in self.episodes:

                if not e.exists():

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

        src = self.file.path
        
        dst = self.dir.child(f'/Season {self.season} Episode {self}.{src.ext()}')

        return src, dst

    def __int__(self):
        return self.episode
    
    def __str__(self):
        return str(self.episode).zfill(2)


Downloadable = list[Movie | Episode | Season]