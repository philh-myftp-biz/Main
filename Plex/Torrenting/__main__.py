from philh_myftp_biz.terminal import Args, Log, ProgressBar
from philh_myftp_biz.web.torrent import qBitTorrent as qbit
from . import VM, driver, PIDstore, Media
from .Scanner import Missing
from time import sleep
from os import getpid

# ===============================================================

queue: list[Media.Movie|Media.Episode] = []

qbit.clear(rm_files=False)

# ===============================================================

while len(queue) < Args['limit']:
    
    try:
        d = next(Missing)
        d.start()
        if d.file:
            queue += [d]
            Log.INFO(f'Downloading File: {d=}')

    except StopIteration, ConnectionAbortedError:
        Log.WARN(exc_info=True)
        break

# ===============================================================

PIDstore.save([f'python-{getpid()}'])

driver.close()

Log.INFO(f'Waiting for downloads: {len(queue)=}')

# ===============================================================

pbar = ProgressBar(
    queue, 
    mode = 'FCOUNTER',
    label = 'Torrents'
)

while len(queue) > 0:

    sleep(1)

    # Clear queue items that have nothing selected
    qbit.clear(True, lambda t: len(t.enabled_files)==0)

    # Sort queue by seeders (most seeded first)
    qbit.sort(lambda t: t.seeders)

    for d in queue:

        if d.torrent and d.file.finished:

            try:

                Log.INFO(f'Download Complete: {d=}')
                
                src, dst = d.paths

                src.copy(dst)

                Log.INFO(f'Copy Complete: {d=}')

                d.finish()

                pbar.step()

                d.file.stop()

                queue.remove(d)

            except FileNotFoundError, OSError, TypeError:
                Log.WARN(exc_info=True)
                d.torrent and d.torrent.start()

        elif d.torrent.errored:
            d.torrent.start()

# ===============================================================

VM.runH('Save', 'Torrenting')
