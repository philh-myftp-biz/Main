from philh_myftp_biz.file import temp, TXT
from philh_myftp_biz.modules import Module
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
        self.src = src
        self.dst = src.chext('mp4')

        self.tmp = temp('encoding', 'mp4')

def isCorrupted(file:Path) -> bool:

    cap = VideoCapture(str(file))

    if cap.isOpened():

        ret, _ = cap.read()

        if ret is None:
            return True

    else:
        return True
