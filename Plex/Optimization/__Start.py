from __init__ import this, QueueItem, ffmpeg, PIDstore
from ffmpeg_progress_yield import FfmpegProgress
from philh_myftp_biz.db import MimeType
from philh_myftp_biz.classOBJ import log
from philh_myftp_biz.pc import cls
from tqdm import tqdm
from os import getpid

#
PIDstore.save(getpid())

#
queue: list[QueueItem] = []

# Iter through descendants of 'E:/Plex/Media/'
for src in this.dir.child('/Media/').descendants():

    # If the path is a video, but not '.mp4'
    if (MimeType.Path(src) == 'video') and (src.ext() != 'mp4'):

        # Append the item to the queue
        queue += [QueueItem(src)]

        print(src)

#
queue.sort(
    key = lambda i: i.size
)

# Iter through all items in the queue
for i in queue:
    
    #
    cls()

    # Print the source and destination paths
    log(i) 

    try:

        #
        ff = FfmpegProgress([

            str(ffmpeg), # Ffmpeg.exe
            
            '-hwaccel', 'auto', # Use GPU

            '-i', str(i.src), # Input Path
            
#            '-map', f'0:v:0', # Video Stream
#            '-c:v', 'h264_nvenc', # Video Codec

#            '-map', f'0:a:{i.streams['audio']['eng']}', # Audio Stream
#            '-c:a', 'copy', # Audio Codec

            str(i.tmp), # Output Path

        ])

        # Progress Bar
        pbar = tqdm(
            total = 100,
            position = 1,
            desc = "Encoding"
        )
        
        #
        for progress in ff.run_command_with_progress():
            
            #
            pbar.update(progress - pbar.n)
        
        #
        i.tmp.move(i.dst)

        #
        i.src.delete()

    except RuntimeError as e:

        stderr: str = e.args[0]

        raise RuntimeError(stderr.strip()) from None