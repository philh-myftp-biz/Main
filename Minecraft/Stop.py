from philh_myftp_biz.terminal import set_package

set_package('E:/Minecraft')

from .World import Worlds

for w in Worlds:
    w.task.stop()

