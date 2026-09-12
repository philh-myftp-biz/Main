from philh_myftp_biz.terminal import Args
from philh_myftp_biz.json import Dict
from philh_myftp_biz.pc import Path

version = "26.1"

this = Path('E:/Minecraft/')

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
