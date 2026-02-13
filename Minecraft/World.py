from philh_myftp_biz.file import YAML, temp, INI
from philh_myftp_biz.web import download, Driver
from typing import Generator, Callable, Literal
from philh_myftp_biz.process import Start
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.json import Dict
from philh_myftp_biz.text import hex
from philh_myftp_biz.pc import Path
from philh_myftp_biz import VERBOSE


def AutoEdition(name: str) -> Generator[Java|Bedrock]:
    """ """

    match World(name)['edition']:

        case 'java':
            return Java(name)
        
        case 'bedrock':
            return Bedrock(name)

CONFIG_TEMPLATE = """
# Edition
# [java, bedrock]
edition: java

# Difficulty
# [peaceful, easy, normal, hard]
difficulty: easy

# Cheats Enabled
# {boolean}
cheats: true

# Gamemode
# [adventure, survival, creative]
gamemode: creative

# Max Players
# {integer}
players: 20

# Message of the Day
# {string}
message: New World

# Player vs Player Enabled
# {boolean}
pvp: true

# Server Port
port:

  # Java Port
  # [{integer}, null]
  java: 25565

  # Bedrock/Geyser Port
  # {integer}
  bedrock: 19132

# Operators
# {list{string}}
operators: []

"""

class World(Path, Dict):

    _args: list[str]

    _ignore: list[str]

    WebFiles: Callable[[], Generator[tuple[Path, Path]]]
    """Get a list of downloaded files to copy"""

    Configure: Callable[[], None]
    """Configure the world"""

    Edition: Literal['Java', 'Bedrock']
    """ """

    def __init__(self, name:str):

        super().__init__(f'E:/Minecraft/Worlds/{name}/')

        config = self.child('config.yaml')

        if not config.exists():
            config.open('w').write(CONFIG_TEMPLATE)
        
        self._var = YAML(config)

    def _WebFiles_Base(self):

        #============================================

        driver = Driver(
            headless = (not VERBOSE),
            fast_load = True
        )

        files: dict[str, str] = {}

        yield driver, files

        #============================================

        for name, url in files.items():

            tmp = temp(hex.encode(self.name()))

            download(url, tmp, False)

            # SRC, DST
            yield tmp, self.child(name)

        #============================================

    def GenFiles(self) -> Generator[Path]:
        """All generated/expendable files in the world folder"""

        #
        for child in self.children():

            #
            if child.seg() not in self._ignore:

                yield child

    def Start(self):
        """Start the World"""

        process = Start(
            args = self._args,
            dir = self
        )

        while process._task is None:
            pass

        return process

    def __repr__(self):
        return f"World('{self.name()}')"

class Java(World):

    Edition = 'Java'

    _args = [
        'java', 
        '-Xmx2G',
        '-jar', 'fabric-server-launch.jar',
        'nogui'
    ]

    _ignore = [
        'world', 
        'config.yaml'
    ]

    def WebFiles(self):
        
        #========================================================================
        # INIT

        base = super()._WebFiles_Base()
        
        driver, files = next(base)

        #========================================================================
        # Geyser

        files['mods/Geyser.jar'] = 'https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/fabric'

        #========================================================================
        # Fabric Server

        # Get Fabric Server Launcher
        driver.open('https://fabricmc.net/use/server/')

        files['fabric-server-launch.jar'] = driver.element('xpath', '/html/body/main/div/article/div/div[1]/main/div[1]/div[4]/a')[0].get_attribute('href')

        #========================================================================
        # JAVA - Floodgate

        # Open the download page for the latest version
        driver.open("https://modrinth.com/mod/floodgate/versions?l=fabric&c=release")

        files['mods/Floodgate.jar'] = driver.element('xpath', "/html/body/div[1]/div[4]/main/div[5]/div[6]/div[3]/section/div[2]/div[3]/div[2]/div[1]/a")[0].get_attribute('href')

        #========================================================================
        # JAVA - Fabric API

        # Open the download page for the latest version
        driver.open("https://modrinth.com/mod/fabric-api/versions?c=release")

        files['mods/Fabric API.jar'] = driver.element('xpath', "/html/body/div[1]/div[4]/main/div[5]/div[6]/div[3]/section/div[2]/div[3]/div[2]/div[1]/a")[0].get_attribute('href')

        #========================================================================

        yield from base

    def Configure(self) -> None:
            
        #======================================================
        # GIT IGNORE

        with self.child('.gitignore').open('w') as file:
        
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
            file.write('world/session.lock')

        #======================================================
        # Agree to EULA

        Log.VERB(f'Agreeing to EULA: {self}')

        eula = Dict(INI(self.child('eula.txt')))

        eula['eula'] = True

        #======================================================
        # Sync server.properties

        Log.VERB(f"Syncing Config: {self} FILE='server.properties'")

        # Wrap the 'server.properties' file
        props = Dict(INI(self.child('server.properties')))

        # Option: difficulty
        props['difficulty'] = self['difficulty']

        # Option: cheats
        props['enable-command-block'] = self['cheats']

        # Option: gamemode
        props['gamemode'] = self['gamemode']

        # Option: players
        props['max-players'] = self['players']

        # Option: message
        props['motd'] = self['message']

        # Option: pvp
        props['pvp'] = self['pvp']

        # Option: port/java
        props['server-port'] = self['port']['java']

        #======================================================

class Bedrock(World):

    Edition = 'Bedrock'

    # TODO