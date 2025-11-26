from philh_myftp_biz.db import MimeType
from __init__ import this, QueueItem
from ffmpeg_wrapper import ffmpeg
from philh_myftp_biz import Args

args = Args()
if len(args) == 1:
    limit = args[0]
else:
    limit = 5

queue: list[QueueItem] = []

for src in this.dir.child('/Media/').descendants():

    if len(queue) == limit:
        break

    elif MimeType.Path(src) == 'video':

        if src.ext() != 'mp4':

            queue += [QueueItem(src)]

for i in queue:
    
    print()
    print(i.src)
    print(i.dst)

    try:

        ffmpeg([
            '-i', str(i.src), # Input Path
            '-c:v', 'h264_nvenc', # Video Codec
            '-c:a', 'copy', # Audio Codec
            str(i.dst), # Output Path
            '-y' # Overwrite Existing File
        ])

        i.src.delete()

    except KeyboardInterrupt:

        i.dst.delete()

        exit()
