from philh_myftp_biz.modules import Module, Service
from philh_myftp_biz import ParsedArgs
from typing import Generator, Literal
from philh_myftp_biz.pc import Path

# Minecraft Module
this = Module('E:/Minecraft')

# Parsed COmmand Line Arguements
args = ParsedArgs()

# Parse Age: name
args.Arg(
    'name',
    'Select Server by name'
)

def Edition(server:Path) -> None | Literal['java', 'bedrock']:
    """
    Assume the edition (java/bedrock) of a server by it's path
    """

    # Wait until args are declared
    for p in server.children():

        # If server is Java Edition
        if p.ext() == 'jar':
            return 'java'
            
        # If server is Bedrock Edition
        elif p.ext() == 'exe':
            return 'bedrock'

def Worlds() -> Generator[Service]:

    # If a name is given
    if args['name']:
    
        # Yield the world folder with the given name
        yield Service(this, f'/Worlds/{args['name']}/')

    #
    else:

        #
        for s in this.dir.child('/Worlds/').children():
            
            #
            if s.isdir():

                yield Service(this, f'/Worlds/{s.name()}/')
    