from philh_myftp_biz.file import temp, YAML
from philh_myftp_biz.modules import Module
from philh_myftp_biz.web import download
from philh_myftp_biz.text import hex
from philh_myftp_biz.pc import Path
from typing import Literal

this = Module('E:/Minecraft')

class Server:

    edition: Literal['java', 'bedrock']

    def __init__(self,
        path: Path
    ):
        self.path = path

        self.config = YAML(path.child('config.yaml')).read()

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

