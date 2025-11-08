from philh_myftp_biz.classOBJ import log
from typing import Generator, Literal
from Instances import this
import Media

def Scanner(
    limit: int
) -> list[Media.Episode | Media.Season | Media.Movie]:
    
    items = []

    for gen in (Movies(), Shows()):

        for item in gen:
            
            #
            if item.valid:

                log(item, 'CYAN')

                item.start()

                items += [item]

            else:

                log(item, 'RED')

            #
            if len(items) == limit:
                return items

def ReadName(
    name: Literal['Title (Year)']
) -> list[str, int]:
    
    # Get title from directory name
    Title = name.split(' (')[0]
    
    # Get year from directory name
    Year = int(name.split('(')[1].split(')')[0])

    return Title, Year

def Movies() -> Generator[Media.Movie]:
    
    for p in this.dir.child('/Media/Movies/').children():

        if p.ext() == 'todo':

            Title, Year = ReadName(p.name())

            yield Media.Movie(Title, Year)

def Shows() -> Generator[Media.Episode | Media.Season]:

    # Loop through all child directories of 'E:/Plex/Media/Shows' 
    for ShowDir in this.dir.child('/Media/Shows').children():

        print('Scanning:', ShowDir)

        Title, Year = ReadName(ShowDir.name())

        # Get Show from title and year 
        show = Media.Show(Title, Year)

        # Iter through all seasons in the show
        for season in show.Seasons():
            
            # Iter through all episodes in the season
            for episode in season.Episodes():

                yield episode