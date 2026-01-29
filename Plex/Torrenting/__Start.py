from __init__ import qbit, VM, driver, args, PIDstore
from philh_myftp_biz.terminal import Log
from Scanner import Downloads
from time import sleep
from os import getpid
import Media

# ===============================================================
# INITIALIZATION

# Start the Virtual Machine
VM.runH('Start', 'Torrenting')

# List of downloads
queue: list[Media._Template] = []

# Clear the download queue
qbit.clear(rm_files=False)

# ===============================================================
# FIND MAGNETS

# Initialize the download generator
downloads = Downloads()

while True:

    try:

        # Get the next download from the generator
        d = next(downloads)

        # Start the download
        d.start()

        # If a valid file has been found
        if d.file:

            Log.INFO(f'Downloading File: {str(d)}')

            # Start downloading the file
            d.file.start()

            # Add the download item to the queue
            queue += [d]

        # If no valid file has been found
        else:

            Log.WARN(f'File Failed to Download: {str(d)}')
    
    # Continue the loop if the download has timed out
    except TimeoutError:

        Log.FAIL('', exc_info=True)

        # Skip to the next download
        continue

    # Break the loop if the generator is exhausted
    except StopIteration:

        # Break the loop
        break

    #
    except ConnectionAbortedError:

        Log.CRIT('', exc_info=True)

        # Break the loop
        break

    # Break the loop if the queue limit has been reached
    if len(queue) >= args['limit']:

        Log.WARN('Download Limit Reached')

        break

# ===============================================================

#
PIDstore.save([f'python-{getpid()}'])

# Close the WebDriver
driver.close()

Log.INFO(f'Waiting for downloads: {len(queue)=}')

# ===============================================================
# MANAGE DOWNLOADS

# Loop until there are no downloads left
while len(queue) > 0:

    sleep(1)

    # Iter through the download queue
    for x, d in enumerate(queue):

        # If the download is finished
        if d.file.finished():

            Log.INFO(f'Download Complete: {str(d)=}')
            
            # Get source and destination paths of file
            src, dst = d.paths()

            # Move the source file to the destination path
            src.copy(dst)

            Log.INFO(f'Copy Complete: {str(d)=}')

            # Run any media-specific final commands for the download
            d.finish()

            # Stop downloading the file
            d.file.stop()

            # Remove the download from the list
            queue.remove(d)

        # If the magnet is errored
        elif d.magnet.errored():

            # Start the download
            d.magnet.start()

# ===============================================================

# Stop the Virtual Machine
VM.runH('Save', 'Torrenting')
