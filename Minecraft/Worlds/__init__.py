from philh_myftp_biz.modules import Module
from philh_myftp_biz.terminal import ParsedArgs
from typing import Generator

from philh_myftp_biz.pc import Path
from philh_myftp_biz.process import SysTask

from philh_myftp_biz.file import PKL
from philh_myftp_biz.json import Dict

# Minecraft Module
this = Module('E:/Minecraft')

#============================================================

# Parsed COmmand Line Arguements
args = ParsedArgs()

# Parse Age: name
args.Arg(
    name = 'world',
    desc = 'Select Specific World'
)

#============================================================

Tasks: Dict[SysTask] = Dict(PKL(
    path = this.dir.child('/__pycache__/Tasks.pkl'),
    default = {}
))

def Worlds() -> Generator[Path]:

    # If a specific world is given
    if args['world']:
    
        # Yield the world folder with the given name
        yield this.dir.child(f'/Worlds/{args['world']}/')

    #
    else:

        #
        for s in this.dir.child('/Worlds/').children():

            # Yield the world folder with the given name
            yield this.dir.child(f'/Worlds/{s.name()}/')
    