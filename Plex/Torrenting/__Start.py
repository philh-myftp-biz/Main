from philh_myftp_biz.terminal import ProgressBar, cls
from __init__ import qbit, VM, driver, args
from philh_myftp_biz.classOBJ import log
from Scanner import Downloads
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

            log(d, 'GREEN')

            # Start downloading the file
            d.file.start()

            # Add the download item to the queue
            queue += [d]

        # If no valid file has been found
        else:

            log(d, 'RED')
    
    # Continue the loop if the download has timed out
    except TimeoutError:

        # Skip to the next download
        continue

    # Break the loop if the generator is exhausted
    except StopIteration:

        # Break the loop
        break

    # Break the loop if the queue limit has been reached
    if len(queue) >= args['limit']:

        break

# ===============================================================

# Close the WebDriver
driver.close()

# Sort the download queue
qbit.sort()

# Clear the terminal window
cls()

# Create a progress bar
pbar = ProgressBar(len(queue))

# ===============================================================
# MANAGE DOWNLOADS

# Loop until there are no downloads left
while len(queue) > 0:

    # Iter through the download queue
    for x, d in enumerate(queue):

        # If the download is finished
        if d.file.finished():
            
            # Get source and destination paths of file
            src, dst = d.paths()

            # Move the source file to the destination path
            src.copy(dst, False)

            # Log the finished download
            log(d, 'GREEN')

            # Run any final commands for the download
            d.finish()

            # Stop downloading the file
            d.file.stop()

            # Remove the download from the list
            del queue[x]

            # Update the progress bar
            pbar.step()

        # If the magnet is errored
        elif d.magnet.errored():

            # Start the download            
            d.magnet.start()

# ===============================================================

# Stop the Virtual Machine
VM.runH('Stop', 'Torrenting')
