from philh_myftp_biz.terminal import Log
from philh_myftp_biz.json import Dict
from philh_myftp_biz.file import INI
from philh_myftp_biz.pc import Path

def Java(
    config: Dict,
    path: Path
):
    
    NAME = path.name()

    #======================================================
    # Agree to EULA

    Log.VERB(f'Agreeing to EULA: {NAME=}')

    eula = Dict(INI(path.child('eula.txt')))

    eula['eula'] = True

    #======================================================
    # Sync server.properties

    Log.VERB(f"Syncing Config: {NAME=} FILE='server.properties'")

    # Wrap the 'server.properties' file
    props = Dict(INI(path.child('server.properties')))

    # Option: difficulty
    props['difficulty'] = config['difficulty']

    # Option: cheats
    props['enable-command-block'] = config['cheats']

    # Option: gamemode
    props['gamemode'] = config['gamemode']

    # Option: players
    props['max-players'] = config['players']

    # Option: message
    props['motd'] = config['message']

    # Option: pvp
    props['pvp'] = config['pvp']

    # Option: port/java
    props['server-port'] = config['port']['java']

    #======================================================


def Bedrock(
    config: Dict,
    path: Path
):
    pass