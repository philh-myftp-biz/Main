from philh_myftp_biz.db import MimeType
from philh_myftp_biz import ParsedArgs
from __init__ import this, QueueItem
from ffmpeg_wrapper import encode

args = ParsedArgs()
args.Arg('limit', 5)

#
queue: list[QueueItem] = []

#
for src in this.dir.child('/Media/').descendants():

    #
    if len(queue) == args['limit']:
        break

    #
    elif MimeType.Path(src) == 'video':

        #
        if src.ext() != 'mp4':

            queue += [QueueItem(src)]

#
for i in queue:
    
    #
    print()
    print(i.src)
    print(i.dst)

    try:

        #
        encode([

            '-i', str(i.src), # Input Path
            
            '-map', f'0:v:0', # Video Stream
            '-c:v', 'h264_nvenc', # Video Codec

            '-map', f'0:a:m:language:eng', # Audio Stream
            '-c:a', 'copy', # Audio Codec

            str(i.dst), # Output Path
            '-y', # Overwrite Existing File

        ])

        #
        i.src.delete()

    #
    except Exception as e:

        i.dst.delete()

        raise e
