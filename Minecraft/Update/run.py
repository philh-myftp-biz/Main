from __init__ import Server, this, File
from philh_myftp_biz.json import Dict
from philh_myftp_biz.file import INI
import Files

for p in this.dir.child('/Worlds/'):
    
    # Wrap the server path
    server = Server(p)

    # Get a list of files to copy
    files: list[File] = getattr(Files, server.edition)

    # Iter through all files for this edition
    for f in files:

        # Source File
        src = f.path

        # Destination File
        dst = server.path.child(f.name)

        # Copy the src file to the dst path
        src.copy(dst)

    # If the edition is java
    if server.edition == 'java':
        
        # Wrap the 'server.properties' file
        props = Dict(INI(server.path.child('server.properties')))

        # Option: difficulty
        props['difficulty'] = server.config['difficulty']

        # Option: cheats
        props['enable-command-block'] = server.config['cheats']

        # Option: gamemode
        props['gamemode'] = server.config['gamemode']

        # Option: players
        props['max-players'] = server.config['players']

        # Option: message
        props['motd'] = server.config['message']

        # Option: pvp
        props['pvp'] = server.config['pvp']

        # Option: port/java
        props['server-port'] = server.config['port']['java']

