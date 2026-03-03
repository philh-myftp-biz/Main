from philh_myftp_biz.process import SysTask
from __init__ import Worlds, PIDs

for w in Worlds():

    task = SysTask(PIDs[w.name])

    task.stop()
