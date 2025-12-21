from philh_myftp_biz.file import ZIP, temp, TXT
from philh_myftp_biz.modules import Module
from philh_myftp_biz.web import download
from philh_myftp_biz.pc import Path
from cv2 import VideoCapture

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
        # ==========================================

        self.src = src
        self.dst = src.chext('mp4')

        self.tmp = temp('encoding', 'mp4')

        self.size = src.size()

        # ==========================================

        self.corrupted: bool = False

        cap = VideoCapture(str(self.src))

        if cap.isOpened():

            ret, _ = cap.read()

            if ret is None:
                self.corrupted = True

        else:
            self.corrupted = True

        cap.release()

#==============================================
# FFMPEG

# Ffmpeg.exe
ffmpeg = temp('ffmpeg', 'exe', '0')

# FFprobe.exe
ffprobe = temp('ffprobe', 'exe', '0')

# If ffmpeg.exe does not exist
if not (ffmpeg.exists() and ffprobe.exists()):

    # ffmpeg.zip
    zipfile = temp('ffmpeg', 'zip')

    # Download ffmpeg
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

    # Extract ffprobe.exe from ffmpeg.zip
    zip.extractFile(
        file = next(zip.search('ffprobe.exe')),
        path = ffprobe
    )

#==============================================
