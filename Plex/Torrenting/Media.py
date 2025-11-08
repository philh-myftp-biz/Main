from philh_myftp_biz.array import intify, priority, filter, max
from Instances import this, tpb, qbit, driver, omdb
from philh_myftp_biz.web import Magnet
from philh_myftp_biz.pc import Path
from difflib import SequenceMatcher
from typing import Generator
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

class Movie(Magnet):

    def __init__(self,
        title: str,
        year: int
    ):
        
        self.Title = title
        self.Year = year
        
        self.valid = True

        # Iter through all existing movie files
        for p in this.dir.child('/Media/Movies/').children():

            # Check if this file is of the current movie
            if self.validName(p.name()):

                if p.ext() == 'todo':
                    self.__todo = p

                else:
                
                    # Invalidate this instance
                    self.valid = False
                    
                    break
        
        if self.valid:

            # Create new ThePirateBay search
            search = tpb.search(

                f'{title} {year}',

                driver = driver,
                qbit = qbit

            )

            magnet = max_magnet(self, list(search))

            if magnet:

                self.valid = True

                super().__init__(
                    title = magnet.title,
                    seeders = magnet.seeders,
                    leechers = magnet.leechers,
                    url = magnet.url,
                    size = magnet.size,
                    qbit = qbit
                )

            else:

                self.valid = False

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

    def paths(self) -> None | Generator[list[Path]]:

        for f in self.files():

            if self.validName(f.path.name()):

                src = Path('E:/Users/philh/Torrenting' + str(f.path)[2:])
                dst = this.dir.child(f"/Movies/['{self.Title}', {self.Year}].{f.path.ext()}")

                return src, dst

    def Finish(self):
        # Delete the placeholder file
        self.__todo.delete()

class Show:

    def __init__(self,
        title: str,
        year: int             
    ):
        
        self.title = title
        self.year = year
        
        # Fetch show details from the Open Movie Database
        self.__data = omdb.show(
            title = title,
            year = year
        )

        self.path = this.dir.child(f"/Media/Shows/{title} ({year})")
        """../Media/Shows/{Title} ({Year})/"""

    def Seasons(self) -> Generator['Season']:
        # Loop through all seasons
        for s in self.__data.Seasons:

            yield Season(
                show = self,
                season = int(s),
                episodes = self.__data.Seasons[s]
            )

class Season(Magnet):

    def __init__(self,
        show: 'Show',
        season: int,
        episodes: list[str]
    ):
        
        self.show = show
        self.season = season
        self.__episodes: list[int] = intify(episodes)

        self.path = show.path.child(f"/Season {self}")
        """../Season {Season}/"""

        return
        # TODO

        # =========================================

        self.__missing_episodes = self.__episodes.copy()

        for p in self.path.children():
            
            data = PTN.parse(p.name())
            
            for x, e in enumerate(self.__missing_episodes):
                if e == data['episode']:
                    
                    del self.__missing_episodes[x]
                    
                    break

        self.valid = (len(self.__missing_episodes) > 0)

        # =========================================

        if self.valid:

            # Create new ThePirateBay search
            search = tpb.search(

                f'{self.show.title} {self.show.year} Season {season}'
                f'{self.show.title} Season {season}',
                f'{self.show.title} s{season}',

                driver = driver,
                qbit = qbit

            )

            #
            magnet = max_magnet(self, list(search))
            
            if magnet:

                super().__init__(
                    title = magnet.title,
                    seeders = magnet.seeders,
                    leechers = magnet.leechers,
                    url = magnet.url,
                    size = magnet.size,
                    qbit = qbit
                )

            else:

                self.valid = False
    
    def validName(self, name:str) -> bool:

        # Parse the file name
        data = PTN.parse(name)

        # Check if the file season is the same
        if 'season' in data:
            season = (data['season'] == int(self.season))
        else:
            season = False

        # Check if the file title is more than 60% similar to the show title
        if Path(name).ext():
            
            # Check if the file episode is the same
            if 'episode' in data:
                episode = (data['episode'] in self.__missing_episodes)
            else:
                episode = False

            return (season and episode)
        
        else:
            title = SequenceMatcher(None,
                a = data['title'], 
                b = self.show.title
            ).ratio() > .6

            return (title and season)

    def paths(self) -> None | Generator[list[Path]]:

        for f in self.files():

            if self.validName(f.path):

                src = Path('E:/Users/philh/Torrenting' + str(f.path)[2:])
                dst = self.path.child(f'/Season {self.season} Episode {self}.{f.path.ext()}')

                yield src, dst

    def Episodes(self) -> Generator['Episode']:
        for e in self.__episodes:
            yield Episode(
                season = self,
                episode = int(e)
            )

    def __int__(self):
        return self.season

    def __str__(self):
        return str(self.season).zfill(2)
    
    def Finish(self):
        pass

class Episode(Magnet):

    def __init__(self,
        season: 'Season',
        episode: int
    ):
        self.season = season
        self.show = season.show
        self.episode = episode

        self.valid = True

        # Loop through all existing episode files
        for p in season.path.children():

            # Check if the file is of this episode
            if self.validName(p.name()):
                
                # Invalidate this instance
                self.valid = False
                
                break

        if self.valid:

            # Create new ThePirateBay search
            search = tpb.search(

                f'{self.show.title} s{season}e{self}',
#                    f'{self.show.title} {self.show.year} Season {season}'
                f'{self.show.title} Season {season}',
                f'{self.show.title} s{season}',

                driver = driver,
                qbit = qbit

            )

            #
            magnet = max_magnet(self, list(search))
            
            if magnet:

                super().__init__(
                    title = magnet.title,
                    seeders = magnet.seeders,
                    leechers = magnet.leechers,
                    url = magnet.url,
                    size = magnet.size,
                    qbit = qbit
                )

            else:

                self.valid = False
    
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

    def paths(self) -> None | Generator[list[Path]]:

        for f in self.files():

            if self.validName(f.path):

                src = Path('E:/Users/philh/Torrenting' + str(f.path)[2:])
                dst = self.season.path.child(f'/Season {self.season} Episode {self}.{f.path.ext()}')

                yield src, dst
            
    def __int__(self):
        return self.episode
    
    def __str__(self):
        return str(self.episode).zfill(2)

    def Finish(self):
        pass