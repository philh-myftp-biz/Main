from philh_myftp_biz.functools import singleton
from philh_myftp_biz.terminal import Args
from philh_myftp_biz.text import contains
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.pc import Path
from typing import Generator, Type
from random import shuffle
from . import Media

def children[T](dir, clazz:Type[T]):

    path = Path(f'E:/Plex/Media/{dir}/')

    dirs = list(filter(
        lambda p: contains.any(p.name, Args['filter']), 
        path.children
    ))
    shuffle(dirs)

    for path in dirs:
        try:

            item = clazz(
                title = path.name.split(' (')[0],
                year = int(path.name.split('(')[1].split(')')[0])
            )

            if path.is_file:
                item.finish = path.delete

            if not item.exists:
                yield item

        except IndexError:
            Log.WARN(exc_info=True)

def notexists[T](items:list[T]) -> 'filter[T]':
    return filter(lambda e: not e.exists, items)

@singleton
def Missing() -> Generator[Media.Movie|Media.Episode, None, None]:

    #==========================================================

    yield from children('Movies', Media.Movie)

    #==========================================================

    for show in children('Shows', Media.Show):

        for season in notexists(show.seasons):
            season.start()
            yield from notexists(season.episodes)

    #==========================================================