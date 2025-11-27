from philh_myftp_biz.pc import cls, ProgressBar
from __init__ import qbit, driver, args, VM
from Scanner import Scanner
import Media

#
cls()

#
if args['verbose']:
    print('\nClearing Download Queue ...')
qbit.clear()

if args['verbose']:
    print('\nDiscovering Magnets ...')

# Create a progress bar
pbar = ProgressBar(args['limit'])

# List of downloads
downloads: Media.Downloadable = []

# Iter through downloads in scanner
for download in Scanner():

    #
    download.file.start(True)

    # Append the download to the list
    downloads += [download]

    #
    pbar.step()

    # If enough downloads have already been started
    if len(downloads) == args['limit']:
        break

#
pbar.stop()

# Close the webdriver
driver.close()

if args['verbose']:
    print('\nDownloading Magnets ...')

# Create a progress bar
pbar = ProgressBar(len(downloads))

# Loop until no downloads are left
while len(downloads) > 0:

    #
    qbit.sort()

    # Iter through all downloads
    for x, d in enumerate(downloads):

        # If the download is finished
        if d.file.finished():
            
            # Get source and destination paths of file
            src, dst = d.paths()

            #
            if args['verbose']:
                print()
                print('src:', src)
                print('dst:', dst)

            # Move the source file to the destination path
            src.copy(
                dst = dst,
                show_progress = args['verbose']
            )

            # Remove the download from the list
            del downloads[x]

            #
            pbar.step()

        if d.magnet.errored():

            if args['verbose']:
                print(f'\nRetrying: {d.magnet.url[:15]}...')
            
            d.magnet.start()

# Power off the Virtual Machine
VM.run(
    'save', 'Torrenting',
    hide = ('vm' not in args['debug'])
)
