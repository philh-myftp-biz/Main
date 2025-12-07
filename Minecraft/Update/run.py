from __init__ import World, this, File, ControlsTempl
from philh_myftp_biz.json import Dict
from philh_myftp_biz.file import INI
import Files

for p in this.dir.child('/Worlds/'):
    
    # Wrap the world
    w = World(p)

    # Copy Controls
    ControlsTempl.copy(w.path)

    #
    wasRunning = w.service.Running()

    #
    w.service.Stop()

    # Get a list of files to copy
    files: list[File] = getattr(Files, w.edition)

    # Iter through all files for this edition
    for f in files:

        # Source File
        src = f.path

        # Destination File
        dst = w.path.child(f.name)

        # Copy the src file to the dst path
        src.copy(dst)

    # If the edition is java
    if w.edition == 'java':
        
        # Wrap the 'server.properties' file
        props = Dict(INI(w.path.child('server.properties')))

        # Option: difficulty
        props['difficulty'] = w.config['difficulty']

        # Option: cheats
        props['enable-command-block'] = w.config['cheats']

        # Option: gamemode
        props['gamemode'] = w.config['gamemode']

        # Option: players
        props['max-players'] = w.config['players']

        # Option: message
        props['motd'] = w.config['message']

        # Option: pvp
        props['pvp'] = w.config['pvp']

        # Option: port/java
        props['server-port'] = w.config['port']['java']

    #
    if wasRunning:
        
        #
        w.service.Start()