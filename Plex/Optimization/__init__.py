from philh_myftp_biz.file import ZIP, temp, TXT
from philh_myftp_biz.modules import Module
from philh_myftp_biz.web import download
from philh_myftp_biz.pc import Path
from philh_myftp_biz import run
from typing import Literal

#==============================================
# Plex Module

# Declare the 'Plex' module
this = Module('E:/Plex')

# Store for execution pid
PIDstore = TXT(this.dir.child('/Optimization/__pycache__/PID.txt'))

#==============================================

class QueueItem:

    streams: dict[str, dict[str, int]] = {

        'audio': {},

        'video': {},

        'subtitle': {}

    }

    def __init__(self,
        src: Path
    ):
        # ==========================================

        self.src = src
        self.dst = src.chext('mp4')

        self.tmp = temp('encoding', 'mp4')

        self.size = src.size()

        # ==========================================
        """
        r = run(
            args = [
                ffprobe,
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_streams',
                '-show_format', 
                self.src
            ],
            wait = True,
            hide = True
        )

        streams: dict[str, dict[str, str]] = r.output('json')['streams']

        for stream in streams:

            if 'tags' in stream:
            
                if 'language' in stream['tags']:

                    lang: str = stream['tags']['language']

                    type: str = stream['codec_type']

                    index = stream['index']

                    self.streams[type][lang] = index
        """
        # ==========================================

#==============================================
# FFMPEG

# Ffmpeg.exe
ffmpeg = temp('ffmpeg', 'exe', '0')

#
ffprobe = temp('ffprobe', 'exe', '0')

# If ffmpeg.exe does not exist
if not (ffmpeg.exists() and ffprobe.exists()):

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

    #
    zip.extractFile(
        file = next(zip.search('ffprobe.exe')),
        path = ffprobe
    )

#==============================================
