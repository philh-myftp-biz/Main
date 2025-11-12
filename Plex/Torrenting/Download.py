from philh_myftp_biz.pc import cls, ProgressBar
from Instances import qbit, driver
from Scanner import Scanner
import Media

max_downloads = 10

cls()

#
print('\nClearing Download Queue ...')
qbit.clear()


print('\nDiscovering Magnets ...')

#
pbar = ProgressBar(max_downloads)

# List of downloads
downloads: Media.Downloadable = []

# Iter through downloads in scanner
for download in Scanner():

    # Append the download to the list
    downloads += [download]

    pbar.step()

    # If enough downloads have already been started
    if len(downloads) == max_downloads:
        break

#
pbar.stop()

# Close the webdriver
driver.close()

print('\nDownloading Magnets ...')

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
            src.copy(dst, False)

            # Remove the download from the list
            del downloads[x]

            #
            pbar.step()
