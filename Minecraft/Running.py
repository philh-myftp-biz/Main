from philh_myftp_biz.terminal import cls, set_package

set_package('E:/Minecraft')

from .World import Worlds

for w in Worlds:
    if w.task.exists:
        cls()
        print('true')
        break

else:    
    cls()
    print('false')