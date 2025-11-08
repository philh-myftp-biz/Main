from philh_myftp_biz.classOBJ import log
from philh_myftp_biz.pc import cls
from Instances import qbit, temp
from Scanner import Scanner
import Media

# Clear the terminal
cls()

print('Clearing Download Queue ...')
qbit.clear()

print('Clearing Temporary Files ...')
for p in temp.children():
    if (not p.inuse()) and p.exists():
        p.delete()

# List of downloads
downloads: list[Media.Movie, Media.Episode, Media.Season] = list(Scanner(1))

print('Waiting for downloads ...')

# Loop until no downloads are left
while len(downloads) > 0:

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
