from philh_myftp_biz.classOBJ import log
from typing import Generator, Literal
from Instances import this
import Media

def ReadName(
    name: Literal['Title (Year)']
) -> list[str, int]:
    
    # Get title from directory name
    Title = name.split(' (')[0]
    
    # Get year from directory name
    Year = int(name.split('(')[1].split(')')[0])

    return Title, Year

def Scanner() -> Generator[Media.Movie | Media.Episode]:

    # The directory with all movie files
    MovieDir = this.dir.child('/Media/Movies/')

    print('Scanning:', MovieDir)
    
    # Iter through all movie files
    for p in MovieDir.children():

        # Check if the file ends with '.todo'
        if p.ext() == 'todo':

            # Get the title and year from the filename
            Title, Year = ReadName(p.name())

            # Create a new movie object
            movie = Media.Movie(Title, Year, p)

            if movie.magnet:
                yield movie

    # Loop through all child directories of 'E:/Plex/Media/Shows' 
    for ShowDir in this.dir.child('/Media/Shows').children():

        print('Scanning:', ShowDir)

        # Get the title and year from the filename
        Title, Year = ReadName(ShowDir.name())

        # Get Show from title and year 
        show = Media.Show(Title, Year)

        # Iter through all seasons in the show
        for season in show.Seasons():

            for episode in season.episodes:

                if episode.magnet:

                    if not episode.exists():

                        yield episode
