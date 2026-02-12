from philh_myftp_biz.modules import Service
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.file import YAML

Worlds = Service('E:/Minecraft/Worlds/')

for world in Worlds.path.children():

    if world.isfile():
        continue

    #==================================================
    # INIT

    NAME = world.name()

    serv: Service = Worlds.Args('--world', NAME)

    Log.INFO(f"Selected World: {NAME=}")

    # Config
    config = YAML(world.child('config.yaml')).read()

    #==================================================
    # IMPORTS

    match config['edition']:

        case 'java':
            from Files import java as files
            from SyncConfig import Java as SyncConfig

        case 'bedrock':
            from Files import bedrock as files
            from SyncConfig import Bedrock as SyncConfig

    #==================================================

    wasRunning = serv.Running()

    serv.Stop()

    #==================================================
    # COPY FILES

    # Iter through all files for this edition
    for name, src in files.items():

        # Destination File
        dst = world.child(name)

        # Copy the src file to the dst path
        src.copy(dst)

    #==================================================
    #

    SyncConfig(world)

    #==================================================
    # RESTORE STATE

    #
    if wasRunning:
        
        #
        world.Start()

    #==================================================