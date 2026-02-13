from philh_myftp_biz.terminal import ParsedArgs
from philh_myftp_biz.process import SysTask
from philh_myftp_biz.modules import Module
from philh_myftp_biz.json import Dict
from philh_myftp_biz.file import PKL
from typing import Generator
from World import Bedrock, Java, AutoEdition

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

Tasks: Dict[SysTask] = Dict(PKL(
    path = this.dir.child('/__pycache__/Tasks.pkl'),
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
        for s in this.dir.child('/Worlds/').children():

            yield AutoEdition(s.name())
