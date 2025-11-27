from philh_myftp_biz.pc import cls, ProgressBar
from philh_myftp_biz.classOBJ import log
from philh_myftp_biz import ParsedArgs
from __init__ import qbit, driver, VM
from Scanner import Scanner
import Media

#
args = ParsedArgs()
args.Arg('limit', 50)

#
driver.debug = args['verbose']

cls()

# Power on the Virtual Machine
VM.run(
    'start', 'Torrenting',
    hide = (not args['verbose'])
)

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

    if args['verbose']:
        log(download)

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
                print(f'\nRetrying Magnet: {d.magnet.url[:15]}...')
            
            d.magnet.start()

# Power off the Virtual Machine
VM.run(
    'save', 'Torrenting',
    hide = (not args['verbose'])
)
