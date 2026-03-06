from philh_myftp_biz.web import download, Driver, FirewallException
from typing import Generator, Callable, Literal
from philh_myftp_biz.file import temp, INI
from philh_myftp_biz.process import Start
from philh_myftp_biz.json import Dict
from philh_myftp_biz.text import hex
from philh_myftp_biz.pc import Path
from philh_myftp_biz import VERBOSE
from re import search

def AutoEdition(name: str) -> Java | Bedrock: # pyright: ignore[reportReturnType]
    
    edition: str = INI(World(name).child('edition.ini')).read()['edition']

    match edition: # pyright: ignore[reportMatchNotExhaustive]

        case 'Java':
            return Java(name)
        
        case 'Bedrock':
            return Bedrock(name)

class World(Path):

    _safe: list[str]
    """Don't Delete these"""

    WebFiles: Callable[[], Generator[tuple[Path, Path]]]
    """Get a list of downloaded files to copy"""

    Configure: Callable[[], None]
    """Configure the world"""

    Start: Callable[[], list[int]]
    """Start the World"""

    Edition: Literal['Java', 'Bedrock']
    """ """

    Port: Callable[[], int]
    """Get the Server Port"""

    _GIT_IGNORE: str
    """ """

    def __init__(self, name:str):

        super().__init__(f'E:/Minecraft/Worlds/{name}/')

    def _WebFiles_Base(self):

        #============================================

        driver = Driver(
            headless = (not VERBOSE),
            eager = True
        )

        files: dict[str, str] = {}

        yield driver, files

        #============================================

        driver.close()

        for name, url in files.items():

            tmp = temp(hex.encode(self.name))

            download(url, tmp, False)

            # SRC, DST
            yield tmp, self.child(name)

        #============================================

    def _Configure(self):

        #======================================================
        # GIT IGNORE

        gitignore = self.child('.gitignore')

        gitignore.open('w').write(self._GIT_IGNORE)

        #======================================================
        # FIREWALL

        fe = FirewallException(f'Minecraft World: {self.name}')
        fe.set(self.Port())

        #======================================================

    def GenFiles(self) -> Generator[Path]:
        """All generated/expendable files in the world folder"""

        for child in self.descendants:

            # If the child is not related to any of the safe files
            if not any([self.child(f).related_to(child) for f in self._safe]):

                yield child

    def _Start_Base(self, *args:str):

        return Start(
            args = args,
            dir = self
        )

    def __repr__(self):
        return f"World('{self.name}')"

class Java(World):

    Edition = 'Java'

    _safe = [
        'world/',
        'server.properties',
        'banned-ips.json',
        'banned-players.json',
        'ops.json',
        'whitelist.json',
        'config/Geyser-Fabric/config.yml',
        'edition.ini'
    ]
    
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

    def Port(self):

        props = self.child('server.properties')

        while not props.exists:
            pass

        r = search(
            pattern = r'\nserver-port=(.*)',
            string = props.open().read()
        )

        return int(r.group(1))

    def Start(self):

        process = super()._Start_Base(
            'java', 
            '-Xmx2G',
            '-jar', 'fabric-server-launch.jar',
            'nogui'
        )

        # Agree to the EULA
        eula = Dict(INI(self.child('eula.txt')))
        eula['eula'] = True

        super()._Configure()

        return process

class Bedrock(World):

    Edition = 'Bedrock'

    # TODO
