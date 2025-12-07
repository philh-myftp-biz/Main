from philh_myftp_biz.file import ZIP, temp, TXT
from philh_myftp_biz.modules import Module
from philh_myftp_biz.web import download
from philh_myftp_biz import ParsedArgs
from philh_myftp_biz.pc import Path

#==============================================
# Parse commandline arguements
args = ParsedArgs()
args.Arg('limit', 5)

#==============================================
# Plex Module

# Declare the 'Plex' module
this = Module('E:/Plex')

# Store for execution pid
PIDstore = TXT(this.dir.child('/Optimization/__pycache__/PID.txt'))

#==============================================

class QueueItem:

    def __init__(self,
        src: Path
    ):
        self.src = src
        self.tmp = temp('encoding', 'mp4')
        self.dst = src.chext('mp4')

#==============================================
# FFMPEG

# Ffmpeg.exe
ffmpeg = temp('ffmpeg', 'exe', '0')

# If ffmpeg.exe does not exist
if not ffmpeg.exists():

    # ffmpeg.zip
    zipfile = temp('ffmpeg', 'zip')

    # Download ffmpeg.zip
    download(
        url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip',
        path = zipfile
    )

    # Wrap ffmpeg.zip
    zip = ZIP(zipfile)

    # Extract ffmpeg.exe from ffmpeg.zip
    zip.extractFile(
        file = next(zip.search('ffmpeg.exe')),
        path = ffmpeg
    )

#==============================================
