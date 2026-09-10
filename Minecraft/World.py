from philh_myftp_biz.web import FirewallException
from philh_myftp_biz.functools import singleton
from philh_myftp_biz.process import Start
from philh_myftp_biz.terminal import Args
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.json import Dict
from philh_myftp_biz.file import INI
from philh_myftp_biz.pc import Path
from . import this, Tasks, java_exe
from re import search

class World:

    def __init__(self, name:str) -> None:
        self.path = Path(f'E:/Minecraft/Worlds/{name}/')
        self.name = self.path.name
        self.child = self.path.child

    def _start(self):
        
        process = Start(
            java_exe, 
            '-Xmx2G',
            '-jar', 'fabric-server-launch.jar',
            'nogui',
            dir = self.path
        )

        Tasks[self.name] = process

        return process

    def start(self) -> Start:
        from .Files import files

        #======================================================

        for name, url in files.items():
            url.download(
                path = self.child(name),
                force = False
            )

        #======================================================

        process = self._start()

        #======================================================
        # GIT IGNORE

        with self.child('.gitignore').open('w') as f:
            f.write("""
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

""")

        #======================================================
        # EULA

        eula = Dict(INI(self.child('eula.txt')))
        eula['eula'] = True

        #======================================================
        # FIREWALL

        fe = FirewallException(f'Minecraft World: {self.name}')
        fe.set(self.port)

        #======================================================

        return process

    @property
    def port(self) -> int:

        props = self.child('server.properties')

        r = search(
            pattern = r'\nserver-port=(.*)',
            string = props.open().read()
        )

        return int(r.group(1))

#================================================================================================

@singleton
class Worlds(list[World]):

    def __init__(self) -> None:
        super().__init__()

        if Args['world']:
            self += Args['world']

        else:
            for s in this.child('/Worlds/').children:
                if s.is_dir:

                    self += s.name

    def __iadd__(self, name:str):

        super().__iadd__([World(name)])

        return self
    
    def __iter__(self):

        _iter = super().__iter__()

        for w in _iter:
            Log.INFO(f"Selected World: {w.name}")
            yield w

#================================================================================================
