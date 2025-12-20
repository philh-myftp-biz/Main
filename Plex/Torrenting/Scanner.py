from __init__ import this, args, pbar, driver
from philh_myftp_biz.classOBJ import log
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

                # If the movie has already been downloaded
                if movie.exists():

                    #
                    movie.finish()

                    if args['verbose']:

                        print('Exists:', movie.queries[0])
                        
                # If the movie has not already been downloaded
                else:

                    # Start the download
                    movie.start()

                    # If a file is downloading
                    if movie.file:

                        log(movie, 'GREEN')
                        
                        yield movie

                    else:

                        log(movie, 'RED')

                        # If a magnet has been found
                        if movie.magnet:

                            # Stop the magnet from downloading
                            movie.magnet.stop()

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

                                log(episode, 'GREEN')

                                yield episode

                            else:
                                log(episode, 'RED')

                        elif args['verbose']:

                            print('Exists:', episode.queries[0])

                elif args['verbose']:

                    print('Exists:', season.queries[0])

def Download(downloads: list[Media._Template]):

    # Iter through downloads in scanner
    for download in Scanner():

        # Start the download
        download.file.start(True)

        # Append the download to the list
        downloads += [download]

        # Step the total of the progress bar
        pbar.step_total()

    # Close the webdriver
    driver.close()
