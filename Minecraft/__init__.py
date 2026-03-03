from philh_myftp_biz.terminal import ParsedArgs
from World import Bedrock, Java, AutoEdition
from philh_myftp_biz.modules import Module
from philh_myftp_biz.json import Dict
from philh_myftp_biz.file import JSON
from typing import Generator

#============================================================

# Minecraft Module
this = Module('E:/Minecraft')

#============================================================

# Parsed Command Line Arguements
args = ParsedArgs()

args.Arg(
    name = 'world',
    desc = 'Select Specific World'
)

#============================================================

PIDs: Dict[int] = Dict(JSON(
    path = this.child('/__pycache__/Tasks.json'),
    default = {}    
))

#============================================================

def Worlds() -> Generator[Bedrock|Java]:

    # If a specific world is given
    if args['world']:

        yield AutoEdition(args['world'])

    #
    else:

        #
        for s in this.child('/Worlds/').children:

            try:
                yield AutoEdition(s.name)
            
            except KeyError, TypeError:
                pass
