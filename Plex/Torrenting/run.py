from __init__ import qbit, driver, args, VM, this
from philh_myftp_biz.pc import ProgressBar
from Scanner import Scanner
import Media

print('\nDiscovering Magnets ...')

# Create a progress bar
pbar = ProgressBar(args['limit'])

# List of downloads
downloads: list[Media._Template] = []

# Iter through downloads in scanner
for download in Scanner():

    # Start the download
    download.file.start(True)

    # Append the download to the list
    downloads += [download]

    # Update the progress bar
    pbar.step()

    # If enough downloads have already been started
    if len(downloads) == args['limit']:
        break

# Stop the progress bar
pbar.stop()

# Close the webdriver
driver.close()

print('\nDownloading Magnets ...')

# Create a progress bar
pbar = ProgressBar(len(downloads))

# Loop until no downloads are left
while len(downloads) > 0:

    # Sort the download queue
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