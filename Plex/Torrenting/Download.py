from philh_myftp_biz.classOBJ import log
from philh_myftp_biz.time import sleep
from philh_myftp_biz.pc import cls
from Instances import qbit, driver
from Scanner import Scanner
from tqdm import tqdm
import Media

cls()

print('\nClearing Download Queue ...\n')
qbit.clear()

# List of downloads
downloads: Media.Downloadable = []

for download in Scanner():

    if len(downloads) == 30:
        break
    
    log(download, 'CYAN')

    downloads += [download]

#
driver.close()

print(f'\nWaiting for downloads ...\n')

pbar = tqdm(
    iterable = range(len(downloads)),
    unit = 'download'
)

# Loop until no downloads are left
while len(downloads) > 0:

    # Wait 1 second
    sleep(2)

    # Iter through all downloads
    for x, d in enumerate(downloads):
        
        # If the download is finished
        if d.file.finished():

            log(d, 'GREEN')
            
            #
            src, dst = d.paths()

            # Move the source file to the destination path
            src.copy(dst)

            # Remove the download from the list
            del downloads[x]

            pbar.update(1)
