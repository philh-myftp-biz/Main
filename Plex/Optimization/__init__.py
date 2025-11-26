from philh_myftp_biz.modules import Module
from philh_myftp_biz.pc import Path

this = Module('E:/Plex')

class QueueItem:

    def __init__(self,
        src: Path
    ):
        self.src = src
        self.dst = src.chext('mp4')
