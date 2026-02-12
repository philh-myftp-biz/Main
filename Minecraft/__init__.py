from philh_myftp_biz.modules import Module, Service
from philh_myftp_biz.terminal import ParsedArgs
from typing import Generator

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

def Worlds() -> Generator[Service]:

    # If a name is given
    if args['name']:
    
        # Yield the world folder with the given name
        yield Service(f'E:/Minecraft/Worlds/{args['world']}/')

    #
    else:

        #
        for s in this.dir.child('/Worlds/').children():

            # Yield the world folder with the given name
            yield Service(f'E:/Minecraft/Worlds/{s.name()}/')
    