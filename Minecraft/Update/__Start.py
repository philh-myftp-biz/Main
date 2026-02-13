from philh_myftp_biz.modules import Service
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.file import YAML
from philh_myftp_biz.json import Dict
from time import sleep

Worlds = Service('E:/Minecraft/Worlds/')

# Reveal Hidden Files
Worlds.path.visibility.show()

# Iter through world folders
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
    #

    for child in world.children():

        if child.seg() not in ['world', 'config.yaml']:

            child.delete()

    #==================================================
    # GIT IGNORE

    with world.child('.gitignore').open('w') as file:
        
        # Hide Everything
        file.write('/*\n')

        # Unhide './Config.yaml'
        file.write('!config.yaml\n')

        # Unhide './world/'
        file.write('!world\n')

        # Hide './world/icon.png'
        file.write('world/icon.png\n')

        # Hide './world/level.dat_old'
        file.write('world/level.dat_old\n')

        # Hide './world/session.lock'
        file.write('world/session.lock\n')

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