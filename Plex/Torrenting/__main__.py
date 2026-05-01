from philh_myftp_biz.web.omdb import MediaNotFoundError
from . import qbit, VM, driver, PIDstore, Media
from philh_myftp_biz.terminal import ParsedArgs
from philh_myftp_biz.terminal import Log
from .Scanner import Downloads
from time import sleep
from os import getpid

# ===============================================================

# List of downloads
queue: list[Media.DOWNLOAD] = []

qbit.randomize_port()

# Clear the download queue
qbit.clear(rm_files=False)

# ===============================================================
# FIND MAGNETS

downloads = Downloads()

while True:

    try:

        # Get the next download from the generator
        d = next(downloads)

        # Start the download
        d.start()

        # If a valid file has been found
        if d.file:

            Log.INFO(f'Downloading File: {d=}')

            # Start downloading the file
            d.file.start()

            # Add the download item to the queue
            queue += [d]

        # If no valid file has been found
        else:

            Log.VERB(f'Magnet Not Found: {d=}')
    
    # Continue the loop if the download has timed out
    except TimeoutError:

        Log.FAIL('', exc_info=True)

        # Skip to the next download
        continue

    except MediaNotFoundError:
        continue

    # Break the loop if the generator is exhausted
    except StopIteration:

        Log.WARN('All Items Scanned')

        break

    #
    except ConnectionAbortedError:

        Log.CRIT('', exc_info=True)

        break

    # Break the loop if the queue limit has been reached
    if len(queue) >= ParsedArgs['limit']:

        Log.WARN('Download Limit Reached')

        break

# ===============================================================

PIDstore.save([f'python-{getpid()}'])

driver.close()

Log.INFO(f'Waiting for downloads: {len(queue)=}')

# ===============================================================
# MANAGE DOWNLOADS

# Loop until there are no downloads left
while len(queue) > 0:

    sleep(1)

    # Clear queue items that have nothing selected
    qbit.clear(
        func = lambda t: (len(t.selected_files) == 0)
    )

    # Sort queue by seeders (most seeded first)
    qbit.sort(
        func = lambda t: t.seeders
    )

    # Iter through the download queue
    for d in queue:

        # If the download is finished
        if d.file.finished:

            try:

                Log.INFO(f'Download Complete: {d=}')
                
                # Get source and destination paths of file
                src, dst = d.paths

                # Move the source file to the destination path
                src.copy(dst)

                Log.INFO(f'Copy Complete: {d=}')

                # Run any media-specific final commands for the download
                d.finish()

                # Stop downloading the file
                d.file.stop()

                # Remove the download from the list
                queue.remove(d)

            except FileNotFoundError, OSError:
                d.magnet.recheck()

        # If the magnet is errored
        elif d.magnet.errored:

            # Start the download
            d.magnet.start()

# ===============================================================

# Stop the Virtual Machine
VM.runH('Save', 'Torrenting')
