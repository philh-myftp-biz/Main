from __init__ import this, QueueItem, ffmpeg, PIDstore, isCorrupted
from ffmpeg_progress_yield import FfmpegProgress
from philh_myftp_biz.pc import cls, print
from philh_myftp_biz.classOBJ import log
from philh_myftp_biz.db import MimeType
from tqdm import tqdm
from os import getpid

#
PIDstore.save(getpid())

#
queue: list[QueueItem] = []

# Iter through descendants of 'E:/Plex/Media/'
for src in this.dir.child('/Media/').descendants():

    # If the path is a video file
    if (MimeType.Path(src) == 'video'):

        i = QueueItem(src)

        # If the source file is corrupted
        if isCorrupted(i.src):

            print(i.src, color='RED')

            # Delete the source file
            i.src.delete()

            # If file is movie
            if str(i.src).startswith('E:/Plex/Media/Movies/'):

                # Placeholder file
                todo = i.src.chext('todo')

                # Create the placeholder file
                todo.open('w')

        # If the file is mkv
        elif src.ext() == 'mkv':

            print(i.src, color='YELLOW')

            # Append the item to the queue
            queue += [i]

        else:

            print(i.src, color='GREEN')

# Sort the files by size (smallest first)
queue.sort(
    key = lambda i: i.src.size()
)

# Progress Bar
pbar = tqdm(
    total = 100,
    position = 1,
    desc = "Encoding"
)

# Iter through all items in the queue
for i in queue:
    
    # Clear the terminal window
    cls()

    pbar.reset()

    # Print the source and destination paths
    log(i) 

    try:

        #
        ff = FfmpegProgress([

            str(ffmpeg), # Ffmpeg.exe
            
            '-hwaccel', 'cuda', # Use GPU

            '-i', str(i.src), # Input Path

            '-c:v', 'h264_nvenc', # Video Codec

            str(i.tmp), # Output Path

        ])

        # Run ffmpeg.exe
        for progress in ff.run_command_with_progress():
            # Update the progress bar
            pbar.update(progress - pbar.n)

        if not isCorrupted(i.tmp):
        
            # Move the encoded file to the destination path
            i.tmp.move(i.dst)

            # Wait for any programs to release the source file
            while i.src.inuse():
                pass

            # Delete the source file
            i.src.delete()

    except RuntimeError:
        pass
