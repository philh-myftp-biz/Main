from __init__ import qbit, args, VM, this, pbar
from philh_myftp_biz import thread
from Scanner import Download
from time import sleep
import Media

# Clear the download queue
qbit.clear(rm_files=False)

# List of downloads
downloads: list[Media._Template] = []

# Scan and download in the background
t = thread(Download, downloads)

# Loop until no downloads are left
while t.running() or (len(downloads) > 0):

    #
    sleep(1)
    
    #
    qbit.sort()

    # Iter through all downloads
    for x, d in enumerate(downloads):

        # If the download is finished
        if d.file.finished():
            
            # Get source and destination paths of file
            src, dst = d.paths()

            # Debug: Print the src and destination
            if args['verbose']:
                print()
                print('src:', src)
                print('dst:', dst)

            # Move the source file to the destination path
            src.copy(
                dst = dst,
                show_progress = args['verbose']
            )

            # Run any final commands for the download
            d.finish()

            # Remove the download from the list
            del downloads[x]

            # Update the progress bar
            pbar.step()

        # If the magnet is errored
        elif d.magnet.errored():

            # Start the download            
            d.magnet.start()

# Clear the download queue
qbit.clear()

# Power off the Virtual Machine
VM.run(
    'save', 'Torrenting',
    hide = (not args['verbose'])
)

# Unlock the Plex module
this.lock.unlock()