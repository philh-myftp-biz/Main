from __init__ import qbit, Scanner, Media, temp
from philh_myftp_biz.classOBJ import log
from philh_myftp_biz.time import sleep
from philh_myftp_biz.pc import cls
from philh_myftp_biz import thread
from philh_myftp_biz.array import List

# Clear the terminal
cls()

print('Clearing Download Queue ...')
qbit.clear()

print('Clearing Temporary Files ...')
for p in temp.children():
    if (not p.inuse()) and p.exists():
        p.delete()

# List of downloads
downloads: List[Media.Episode | Media.Movie] = List()

def find_downloads(downloads:List):

    for download in Scanner():

        # Start the download
        download.start()

        # Append the download to the list
        downloads += download

#
t = thread(
    func = find_downloads,
    downloads = downloads
)

# Loop until no downloads are left
while True:

#    if (not t.is_alive()) and (len(downloads) == 0):
#        break

    # Iter through all downloads
    for x, download in enumerate(downloads):
        
        # If the download is finished
        if download.finished():

            #
            log(download, 'GREEN')
            
            # Get the source and destination paths
            for src, dst in download.paths():

                # Move the source file to the destination path
                print()
                print(src)
                print(dst)

                src.move(dst)

            # Stop the download
            download.stop()

            # Remove the download from the list
            del downloads[x]

        # If the download is errored
        elif download.errored():
            
            # Restart the download
            download.restart()

        # If download is still downloading
        elif download.downloading():

            # Loop through all of the downloading files
            for file in download.files():

                # If the file does not have a valid name
                if not download.validName(file.path.name()):
                    
                    # Stop the file from downloading
                    file.stop()