from philh_myftp_biz.modules import Module
from philh_myftp_biz.terminal import Args
from philh_myftp_biz.json import Dict

version = "26.1"

#============================================================

# Minecraft Module
this = Module('E:/Minecraft/')

java_exe = this.child('/.java/bin/java.exe')

#============================================================

Args.Arg(
    name = 'world',
    desc = 'Select Specific World'
)

Args.Flag(
    name = 'force',
    letter = 'f'
)

#============================================================

PIDs: Dict[int] = this.child('/__pycache__/PIDS.json').JSON.Dict

#============================================================
