from __init__ import this, args
from typing import Generator, Literal
import Media

def ReadName(
    name: Literal['Title (Year)']
) -> list[str, int]:
    """
    Get Title and Year from file/folder name

    EXAMPLE:
    ReadName('Test (2025)') -> 'Test', 2025
    """
    
    # Get title from directory name
    Title = name.split(' (')[0]
    
    # Get year from directory name
    Year = int(name.split('(')[1].split(')')[0])

    return Title, Year

def Downloads() -> Generator[Media._Template]:
    """
    Generate a list of Movie or Episode Downloads
    """

    # Iter through all movie files
    for p in this.dir.child('/Media/Movies/').children():

        # If the file name matches the filter
        if args['filter'] in p.name().lower():

            # Check if the file ends with '.todo'
            if p.ext() == 'todo':

                yield Media.Movie(*ReadName(p.name()), p)

    # Loop through all child directories of 'E:/Plex/Media/Shows' 
    for ShowDir in this.dir.child('/Media/Shows').children():

        # If the folder name matches the filter
        if args['filter'] in ShowDir.name().lower():

            # Get Show from the filename 
            show = Media.Show(*ReadName(ShowDir.name()))

            # Iter through all seasons in the show
            for season in show.Seasons():

                yield season

                # Iter through all episodes in the season
                for episode in season.episodes:

                    yield episode
