from philh_myftp_biz.web.minecraft import ModrinthMod, FabricMC
from philh_myftp_biz.web import FirewallException, URL
from philh_myftp_biz.process import Start
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.json import Dict
from philh_myftp_biz.file import INI
from philh_myftp_biz.pc import Path
from . import this, args, PIDs
from typing import Callable
from re import search

class World(Path):

    port: Callable[[], int]
    """Get the Server Port"""

    _GIT_IGNORE: str

    def __init__(self, name:str):
        super().__init__(f'E:/Minecraft/Worlds/{name}/')

    def _update(self):

        #============================================

        files: dict[str, str] = {}

        yield files

        #============================================

        for name, url in files.items():

            dst = self.child(name)

            URL(url).cache(dst)

        #============================================

    def _start(self, *args:str):
        
        #======================================================

        process = Start(args, dir=self)

        PIDs[self.name] = process._process.pid

        #======================================================
        # GIT IGNORE

        gitignore = self.child('.gitignore')

        with gitignore.open('w') as f:
            f.write(self._GIT_IGNORE)

        #======================================================
        # FIREWALL

        fe = FirewallException(f'Minecraft World: {self.name}')
        fe.set(self.port)

        #======================================================

        yield process

    def __repr__(self):
        return f"World('{self.name}')"

class Java(World):

    _GIT_IGNORE = """
# Hide Everything
/*

# Unhide Main Configuration Files
!server.properties
!banned-ips.json
!banned-players.json
!ops.json
!whitelist.json
!edition.ini

# Unhide World Save Data
!world

# Hide Certain Files in Save Data Folder
world/icon.png
world/session.lock

# Unhide Geyser Configuration
!config
/config/*
!/config/Geyser-Fabric
/config/Geyser-Fabric/*
!/config/Geyser-Fabric/config.yml

"""

    def update(self):
        
        base = super()._update()

        files: dict[str, str] = next(base)

        #========================================================================
        # Geyser

        files['mods/Geyser.jar'] = 'https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/fabric'

        #========================================================================
        # Fabric Server

        files['fabric-server-launch.jar'] = FabricMC().serverURL

        #========================================================================
        # JAVA - Floodgate

        files['mods/Floodgate.jar'] = ModrinthMod('floodgate').url

        #========================================================================
        # JAVA - Fabric API

        files['mods/Fabric API.jar'] = ModrinthMod('fabric-api').url

        #========================================================================

        next(base, None)

    @property
    def port(self) -> int:

        props = self.child('server.properties')

        while not props.exists:
            pass

        r = search(
            pattern = r'\nserver-port=(.*)',
            string = props.open().read()
        )

        return int(r.group(1))

    def start(self) -> Start:

        base = super()._start(
            'java', 
            '-Xmx2G',
            '-jar', 'fabric-server-launch.jar',
            'nogui'
        )

        # Agree to the EULA
        eula = Dict(INI(self.child('eula.txt')))
        eula['eula'] = True

        return next(base) # pyright: ignore[reportReturnType]

class Bedrock(World):
    ... # TODO

#================================================================================================

class _Worlds(list[Java|Bedrock]):

    def __iadd__(self, name:str):

        Log.INFO(f"Selected World: {name}")

        edition_ini = INI(Path(f'E:/Minecraft/Worlds/{name}/edition.ini'))

        match edition_ini.read()['edition']: # pyright: ignore[reportMatchNotExhaustive]

            case 'Java':
                world = Java(name)
            
            case 'Bedrock':
                world = Bedrock(name)

        super().__iadd__([world]) # pyright: ignore[reportPossiblyUnboundVariable]

        return self

Worlds = _Worlds()

#================================================================================================

# If a specific world is given
if args['world']:

    Worlds += args['world']

else:

    for s in this.child('/Worlds/').children:

        if s.seg()[0] != '.':

            Worlds += s.name

#================================================================================================
