from philh_myftp_biz.process.SysTask import SysTask
from philh_myftp_biz.web import FirewallException
from philh_myftp_biz.terminal import Args
from philh_myftp_biz.process import Start
from philh_myftp_biz.pc import Path
from . import this, PIDs

_README = """
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

class World:

    def __init__(self, name:str) -> None:

        self.name = name
        self.path = this.child(f'/Worlds/{name}/')

        self.firewall_exception = FirewallException(f'Minecraft World: {self.name}')

        self.gitignore = self.path.child('.gitignore').TXT

        self.eula = self.path.child('eula.txt').INI.Dict

        self.props = self.path.child('server.properties').INI.Dict

    @property
    def task(self) -> SysTask:
        return SysTask(PIDs[self.name])

    def start(self):
        
        process = Start(
            'E:/Minecraft/.java/bin/java.exe',
            '-Xmx2G',
            '-jar', 'fabric-server-launch.jar',
            'nogui',
            dir = self.path
        )

        PIDs[self.name] = process._process.pid

        return process

    def install(self) -> None:
        from .Files import files

        for name, url in files.items():
            url.download(
                path = self.path.child(name),
                force = False
            )

        self.gitignore.save(_README)

        self.eula['eula'] = True

        self.firewall_exception.set( self.props['server-port'] )

#================================================================================================

def _Worlds():

    if Args['world']:
        yield World(name=Args['world'])
        return

    for s in Path('E:/Minecraft/Worlds/').children:
        if s.is_dir:
            yield World(name=s.name)

Worlds = list(_Worlds())

#================================================================================================
