from philh_myftp_biz.file import temp, TXT
from philh_myftp_biz.modules import Module
from philh_myftp_biz.pc import Path
from pymediainfo import MediaInfo
from cv2 import VideoCapture

#==============================================
# Plex Module

# Declare the 'Plex' module
this = Module('E:/Plex')

# Store for execution pid
PIDstore = TXT(this.child('/Optimization/__pycache__/PID.txt'))

#==============================================

class QueueItem:

    def __init__(self,
        src: Path
    ):
        self.src = src
        self.dst = src.chext('mp4')
        self.tmp = temp('encoding', 'mp4')

        # ===========================================

        self.is_corrupted = False

        cap = VideoCapture(str(src))

        if cap.isOpened():

            if cap.read()[0] is None:

                self.is_corrupted = True

        else:

            self.is_corrupted = True
    
        # ===========================================

        self.is_h264 = False
        self.is_h265 = False

        for track in MediaInfo.parse(str(src)).tracks:
            
            if track.track_type == 'Video':

                if (track.format == "AVC") or (track.codec_id == "avc1"):
                    self.is_h264 = True
                
                elif (track.format == "HEVC") or (track.codec_id == "hvc1"):
                    self.is_h265 = True

                break

        # ===========================================
