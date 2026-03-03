from __init__ import this, QueueItem, PIDstore
from ffmpeg_progress_yield import FfmpegProgress
from philh_myftp_biz.terminal import cls, print
from philh_myftp_biz.programs import FFMPEG
from philh_myftp_biz.classOBJ import log
from philh_myftp_biz.db import MimeType
from tqdm import tqdm
from os import getpid

#
PIDstore.save(getpid())

# Progress Bar
pbar = tqdm(
    total = 100,
    position = 1,
    desc = "Encoding"
)

# Iter through descendants of 'E:/Plex/Media/'
for src in this.child('/Media/Shows/The Walking Dead (2010)/Season 07').descendants:

    # If the path is a video file
    if (MimeType.Path(src) == 'video'):

        i = QueueItem(src)

        # If the file is mkv
        if (i.is_h264 or i.is_h265) and (not i.is_corrupted):

            print(i.src)

        else:

            pbar.reset()

            # Print the source and destination paths
            log(i)

            input('..')

            continue

            try:

                #
                ff = FfmpegProgress([

                    str(FFMPEG()), # Ffmpeg.exe
                    
                    '-hwaccel', 'cuda', # Use GPU

                    '-i', str(i.src), # Input Path

                    '-c:v', 'h265_nvenc', # Video Codec

                    '-c:a', 'aac', # Audio Codec

                    str(i.tmp), # Output Path

                ])

                # Run ffmpeg.exe
                for progress in ff.run_command_with_progress():
                    
                    # Update the progress bar
                    pbar.update(progress - pbar.n)
                
                # Move the encoded file to the destination path
                i.tmp.move(i.dst)

                # Wait for any programs to release the source file
                while i.src.inuse():
                    pass

                # Delete the source file
                i.src.delete()

            except RuntimeError:
                pass
