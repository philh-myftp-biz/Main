from philh_myftp_biz.process import SysTask
from .World import Worlds, PIDs

for w in Worlds:

    task = SysTask(PIDs[w.name])

    task.stop()
