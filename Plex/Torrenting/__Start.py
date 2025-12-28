from philh_myftp_biz.terminal import ProgressBar
from philh_myftp_biz.classOBJ import log
from __init__ import qbit, args, VM
from Scanner import Downloads
from time import sleep
import Media

# Start the Virtual Machine
VM.run('Start', 'Torrenting')

# List of downloads
queue: list[Media._Template] = []

# Create a progress bar
pbar = ProgressBar(0)

# Clear the download queue
qbit.clear(rm_files=False)

# Loop until the thread stops and there are no downloads left
while True:

    for d in Downloads():

        # If the item is not already downloading and does not already exist 
        if not (any([(d.queries == i.queries) for i in queue]) and d.exists()):

            # Start the download
            d.start()

            # If a valid file has been found
            if d.file:

                log(d, 'GREEN')

                # Start downloading the file
                d.file.start()

                # Add the download item to the queue
                queue += [d]
                
                # Step the total of the progress bar
                pbar.step_total()

            else:
                log(d, 'RED')

    # ===============================================================

    #
    qbit.sort()

    # ===============================================================

    # Iter through all downloads
    for x, d in enumerate(queue):

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
            del queue[x]

            # Update the progress bar
            pbar.step()

        # If the magnet is errored
        elif d.magnet.errored():

            # Start the download            
            d.magnet.start()

    # ===============================================================

    # Wait 5 minutes
    sleep(60 * 5)
