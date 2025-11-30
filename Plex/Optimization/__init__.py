from ffmpeg_progress_yield import FfmpegProgress
from philh_myftp_biz.modules import Module, ModuleLockedError
from philh_myftp_biz.file import ZIP, temp
from philh_myftp_biz.web import download
from philh_myftp_biz import ParsedArgs
from philh_myftp_biz.pc import Path
from tqdm import tqdm

#==============================================
# Parse commandline arguements
args = ParsedArgs()
args.Arg('limit', 5)

#==============================================
# Plex Module

# Declare the 'Plex' module
this = Module('E:/Plex')

# If the Plex module is locked
if this.lock.locked():
    # Raise Error
    raise ModuleLockedError(this)

else:
    # Lock the Plex module
    this.lock.lock()

#==============================================

class QueueItem:

    def __init__(self,
        src: Path
    ):
        self.src = src
        self.dst = src.chext('mp4')

#==============================================
# FFMPEG

ffmpeg = temp('ffmpeg', 'exe', '0')

#
if not ffmpeg.exists():

    #
    zipfile = temp('ffmpeg', 'zip')

    #
    download(
        url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip',
        path = zipfile
    )

    #
    zip = ZIP(zipfile)

    #
    zip.extractFile(
        file = next(zip.search('ffmpeg.exe')),
        path = ffmpeg
    )

#==============================================
# ENCODER

def encode(i:QueueItem):

    try:

        cmd = [

            str(ffmpeg), # Ffmpeg.exe
            
            '-hwaccel', 'auto', # Use GPU

            '-i', str(i.src), # Input Path
            
            '-map', f'0:v:0', # Video Stream
            '-c:v', 'h264_nvenc', # Video Codec

            '-map', f'0:a:m:language:eng', # Audio Stream
            '-c:a', 'copy', # Audio Codec

            str(i.dst), # Output Path
            '-y', # Overwrite Existing File

        ]

        pbar = tqdm(
            total = 100,
            position = 1,
            desc = "Encoding"
        )
        
        ff = FfmpegProgress(cmd)

        for progress in ff.run_command_with_progress():
            pbar.update(progress - pbar.n)

    except RuntimeError as e:

        stderr: str = e.args[0]

        raise RuntimeError(stderr.strip()) from None

#==============================================