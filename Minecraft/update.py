from __init__ import Server, this, File
from philh_myftp_biz.file import INI
from philh_myftp_biz.json import Dict
import Files

for p in this.dir.child('/Worlds/'):
    
    server = Server(p)

    files: list[File] = getattr(Files, server.edition)

    for f in files:

        src = f.path
        dst = server.path.child(f.name)

        src.copy(dst)

    if server.edition == 'java':
        
        props = Dict(INI(server.path.child('server.properties')))

        props['difficulty'] = server.config['difficulty']

        props['enable-command-block'] = server.config['cheats']

        props['gamemode'] = server.config['gamemode']

        props['max-players'] = server.config['players']

        props['motd'] = server.config['message']

        props['pvp'] = server.config['pvp']

        props['server-port'] = server.config['port']['java']

