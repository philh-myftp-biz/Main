from philh_myftp_biz.modules import Module, Service
from philh_myftp_biz.file import temp, YAML
from philh_myftp_biz.web import download
from philh_myftp_biz.text import hex
from philh_myftp_biz.pc import Path
from typing import Literal

# Minecraft Module
this = Module('E:/Minecraft')

#
ControlsTempl = this.dir.child('/Update/Controls Template/')

class World:
    """
    Minecraft World

    "E:/Minecraft/Worlds/{}/"
    """

    edition: Literal['java', 'bedrock']

    def __init__(self,
        path: Path
    ):

        self.path = path

        self.config = YAML(path.child('config.yaml')).read()

        self.service = Service(this, f'/Worlds/{path.name()}')

        for p in path.children():
            
            if p.ext() == 'jar':
                self.edition = 'java'
                break
            
            elif p.ext() == 'exe':
                self.edition = 'bedrock'
                break

class File:

    def __init__(self,
        name: str,
        url: str
    ):
        
        self.name = name

        self.path = temp(
            name = hex.encode(name),
            ext = self.name[self.name.rfind('.'):]
        )

        download(
            url = url,
            path = self.path
        )

