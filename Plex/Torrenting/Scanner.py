from philh_myftp_biz.terminal import ParsedArgs
from philh_myftp_biz.text import contains
from philh_myftp_biz.terminal import Log

from typing import Generator, Literal
from . import this, Media

def _FILTER(name:str):

    if ParsedArgs['filter'] == '':
        return True
    else:
        return contains.any(name, ParsedArgs['filter'])

def ReadName(
    name: Literal['Title (Year)']
) -> tuple[str, int]:
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

def Downloads() -> Generator[Media.DOWNLOAD]:
    """Generate a list of Movie and Episode Downloads"""

    #==========================================================
    # MOVIES

    # Iter through all child directories of 'E:/Plex/Media/Movies/'
    for p in this.child('/Media/Movies/').children:

        FILTER = _FILTER(p.name)
        TODO = (p.ext == 'todo')

        # If the file name matches the filter
        if FILTER and TODO:

            movie = Media.Movie(*ReadName(p.name), p)

            # If the movie is already downloaded
            if movie.exists:

                Log.INFO(f'Movie Exists\n{movie.Title=}\n{movie.Year=}')

            # If the movie is missing
            else:

                Log.WARN(f'Movie Missing\n{movie.Title=}\n{movie.Year=}')

                yield movie

    #==========================================================
    # EPISODES

    # Iter through all child directories of 'E:/Plex/Media/Shows/'
    for ShowDir in this.child('/Media/Shows/').children:

        # If the folder name matches the filter
        if _FILTER(ShowDir.name):

            # Get Show from the filename 
            show = Media.Show(*ReadName(ShowDir.name))

            Log.VERB(f'Scanning Show\n{show=}\n{ShowDir=}')

            # Iter through all seasons in the show
            for season in show.seasons:

                # If the season is already completely downloaded
                if season.exists:

                    Log.INFO(f'Season Exists\n{show=}\n{season=}')

                # If the season is missing episodes
                else:

                    # Attempt to start downloading the season
                    try:
                        season.start()
                        
                    except TimeoutError:
                        Log.FAIL('', exc_info=True)

                    # Iter through all episodes in the season
                    for episode in season.episodes:

                        # If the episode is already downloaded
                        if episode.exists:

                            Log.INFO(f'Episode Exists\n{show=}\n{season=}\n{episode=}')

                        # If the episode is missing
                        else:

                            Log.WARN(f'Episode Missing\n{show=}\n{season=}\n{episode=}')

                            yield episode

    #==========================================================