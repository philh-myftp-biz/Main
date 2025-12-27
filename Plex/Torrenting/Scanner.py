from philh_myftp_biz.classOBJ import log
from __init__ import this, args
from typing import Generator, Literal
from philh_myftp_biz.terminal import ProgressBar
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

def DOWNLOADS() -> Generator[Media._Template]:
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

                # Iter through all episodes in the season
                for episode in season.episodes:

                    yield episode

def Download(
    queue: list[Media._Template],
    pbar: ProgressBar
):

    while True:

        for d in DOWNLOADS():

            # If the item is not already downloading
            if not any([(d.queries == i.queries) for i in queue]):

                if not d.exists():

                    # Start the download
                    d.start()

                    # If a file is downloading
                    if d.file:

                        log(d, 'GREEN')

                        d.file.start()

                        queue += [d]
                        
                        # Step the total of the progress bar
                        pbar.step_total()

                    else:
                        log(d, 'RED')

                elif args['verbose']:
                    print('Exists:', d.queries[0])
