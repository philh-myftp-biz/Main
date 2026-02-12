from philh_myftp_biz.file import INI, YAML
from philh_myftp_biz.json import Dict
from philh_myftp_biz.file import Path

def Java(path: Path):

    #======================================================

    # Wrap the 'server.properties' file
    props = Dict(INI(path.child('server.properties')))

    # Wrap the 'config.yaml' file
    config = YAML(path.child('config.yaml')).read()
    
    #======================================================

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


def Bedrock(path: Path):
    pass