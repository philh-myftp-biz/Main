from philh_myftp_biz.process import SysTask
from __init__ import Worlds, PIDs

for w in Worlds():

    task = SysTask(PIDs[w.name])

    if task.exists:

        print('true')
        
        break

# If no worlds are running
else:
    
    print('false')