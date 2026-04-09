from philh_myftp_biz.terminal import ParsedArgs
from philh_myftp_biz.modules import Module
from philh_myftp_biz.json import Dict
from philh_myftp_biz.file import JSON

#============================================================

# Minecraft Module
this = Module('E:/Minecraft/')

#============================================================

# Parsed Command Line Arguements
args = ParsedArgs()

args.Arg(
    name = 'world',
    desc = 'Select Specific World'
)

#============================================================

PIDs: Dict[int] = Dict(JSON(this.child('/__pycache__/Tasks.json')))

#============================================================
