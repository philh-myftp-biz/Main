from philh_myftp_biz.classOBJ import log
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

def Scanner() -> Generator[Media._Template]:
    """
    Generate a list of Movie or Episode Downloads
    """

    # Iter through all movie files
    for p in this.dir.child('/Media/Movies/').children():

        # If the file name matches the filter
        if args['filter'] in p.name().lower():

            # Check if the file ends with '.todo'
            if p.ext() == 'todo':

                # Create a new movie object
                movie = Media.Movie(*ReadName(p.name()), p)

                # If the movie has not already been downloaded
                if not movie.exists():

                    # Start the download
                    movie.start()

                    # If a file is downloading
                    if movie.file:

                        # Debug: Log the movie
                        if args['verbose']:
                            log(movie, 'GREEN')
                        
                        yield movie

                    else:

                        # If a magnet has been found
                        if movie.magnet:

                            # Stop the magnet from downloading
                            movie.magnet.stop()

                        # Debug: Log the movie        
                        if args['verbose']:
                            log(movie, 'RED')

    # Loop through all child directories of 'E:/Plex/Media/Shows' 
    for ShowDir in this.dir.child('/Media/Shows').children():

        # If the folder name matches the filter
        if args['filter'] in ShowDir.name().lower():

            # Get Show from the filename 
            show = Media.Show(*ReadName(ShowDir.name()))

            # Iter through all seasons in the show
            for season in show.Seasons():

                # If the season is missing episodes
                if not season.exists():

                    # Start downloading the season
                    season.start()

                    # Iter through all episodes in the season
                    for episode in season.episodes:

                        # If the episode is missing
                        if not episode.exists():

                            # Start downloading the episode
                            episode.start()

                            # If a file is downloading
                            if episode.file:

                                # Debug: Log the Episode
                                if args['verbose']:
                                    log(episode, 'GREEN')

                                yield episode

                            # Debug: Log the Episode
                            elif args['verbose']:
                                log(episode, 'RED')
