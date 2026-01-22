from philh_myftp_biz.terminal import Log
from typing import Generator, Literal
from __init__ import this, args
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
    Generate a list of Movie and Episode Downloads
    """

    #==========================================================
    # MOVIES

    # Iter through all movie files
    for p in this.dir.child('/Media/Movies/').children():

        # If the file name matches the filter
        if args['filter'] in p.name().lower():

            # Check if the file ends with '.todo'
            if p.ext() == 'todo':

                movie = Media.Movie(*ReadName(p.name()), p)

                if movie.exists():

                    Log.INFO(f'Media Exists: {str(movie)}')

                else:

                    yield movie

        else:

            Log.INFO(f'Skipping Media: {p}')

    #==========================================================
    # EPISODES

    # Loop through all child directories of 'E:/Plex/Media/Shows' 
    for ShowDir in this.dir.child('/Media/Shows').children():

        # If the folder name matches the filter
        if args['filter'] in ShowDir.name().lower():

            # Get Show from the filename 
            show = Media.Show(*ReadName(ShowDir.name()))

            # Iter through all seasons in the show
            for season in show.seasons:

                if season.exists():

                    Log.INFO(f'Media Exists: {str(season)}')

                else:

                    season.start()

                    # Iter through all episodes in the season
                    for episode in season.episodes:

                        if episode.exists():

                            Log.INFO(f'Media Exists: {str(episode)}')

                        else:
                            
                            yield episode

        else:

            Log.INFO(f'Skipping Media: {ShowDir}')

    #==========================================================