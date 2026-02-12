from philh_myftp_biz.modules import Service
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.file import YAML
from philh_myftp_biz.json import Dict
from time import sleep

Worlds = Service('E:/Minecraft/Worlds/')

for world in Worlds.path.children():

    if world.isfile() or world.name().startswith('__'):
        continue

    #==================================================
    # INIT

    NAME = world.name()

    serv: Service = Worlds.Args('--world', NAME)

    Log.INFO(f"Selected World: {NAME=}")

    # Config
    config = Dict(YAML(world.child('config.yaml')))

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

    try:
        SyncConfig(config, world)

    except:

        Log.FAIL('', exc_info=True)

        serv.Start()

        sleep(10)

        serv.Stop()

    #==================================================
    # RESTORE STATE

    #
    if wasRunning:
        
        #
        serv.Start()

    #==================================================