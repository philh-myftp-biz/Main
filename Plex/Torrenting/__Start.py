from qbittorrentapi.exceptions import NotFound404Error
from __init__ import qbit, args, pbar, PIDstore
from philh_myftp_biz.terminal import warn
from philh_myftp_biz.process import thread
from Scanner import Download, Queue
from time import sleep
from os import getpid

# Store the pid of the current execution
PIDstore.save(getpid())

# Clear the download queue
qbit.clear(rm_files=False)

# Scan for downloads in the background
t = thread(Download)

# Loop until the thread stops and there are no downloads left
while True:

    #
    sleep(1)

    try:
    
        #
        qbit.sort()

        # Iter through all downloads
        for x, d in enumerate(Queue):

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
                del Queue[x]

                # Update the progress bar
                pbar.step()

            # If the magnet is errored
            elif d.magnet.errored():

                # Start the download            
                d.magnet.start()

    except (NotFound404Error, IndexError) as e:
        warn(e)
