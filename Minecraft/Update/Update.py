from philh_myftp_biz.modules import Service
from philh_myftp_biz.file import YAML
from philh_myftp_biz.pc import Path
import Files

from philh_myftp_biz.terminal import Log

for p in Path('E:/Minecraft/Worlds/').children():

    #==================================================
    # INIT

    Log.INFO(f"Selected World: world='{p.name()}'")
    
    # Wrap the world
    world = Service(p)

    # Config
    config = YAML(world.path.child('config.yaml')).read()

    #==================================================
    # STATUS

    # Check if the world is currently running
    wasRunning = world.Running()

    Log.VERB(f"World is Running: {wasRunning} | world='{p.name()}'")

    try:
        # Stop the world
        world.Stop()
    except FileNotFoundError:
        Log.WARN('', exc_info=True)

    #==================================================
    # COPY FILES

    # Get a list of files to copy
    files: dict[str, Path] = getattr(Files, config['edition'])

    # Iter through all files for this edition
    for name, src in files.items():

        # Destination File
        dst = world.path.child(name)

        # Copy the src file to the dst path
        src.copy(dst)

    #==================================================
    # RESTORE STATE

    #
    if wasRunning:
        
        #
        world.Start()

    #==================================================