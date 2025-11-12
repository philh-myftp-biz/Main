
from philh_myftp_biz.web import Driver, download
from philh_myftp_biz.text import hex
from philh_myftp_biz.file import temp
from typing import Literal
import os, time, urllib

driver = Driver()

class Server:

    def __init__(self,
                 
                 
        version = Literal['java', 'bedrock']
    ):
        
        self.version = version

        self.files: list[File] = []

        for file in files:
            if file.version == version:
                self.files += [file]

class File:

    def __init__(self,
        name: str,
        url: str,
        version: Literal['java', 'bedrock']
    ):
        
        self.name = name
        self.version = version

        self.file = temp(
            name = hex.encode(name),
            ext = self.name[self.name.rfind('.'):]
        )

        download(
            url = url,
            path = self.file
        )

    def copy(self, server:Server):
        pass

files: list[File] = []

File(
    name = 'mods/Geyser.jar',
    url = 'https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/fabric',
    version = 'java'
)

driver.open('https://fabricmc.net/use/server/')
File(
    name = 'fabric-server-launch.jar',
    url = driver.element('xpath', '/html/body/main/div/article/div/div[1]/main/div[1]/div[4]/a')[0].get_attribute('href'),
    version = 'java'
)

driver.open("https://modrinth.com/mod/floodgate/versions?l=fabric")
File(
    name = 'mods/Floodgate.jar',
    url = driver.element('xpath', "/html/body/div[1]/div[4]/main/div[5]/div[6]/div[3]/section/div[2]/div[3]/div[2]/div[1]/a")[0].get_attribute('href'),
    version = 'java'
)

driver.open("https://www.curseforge.com/minecraft/mc-mods/fabric-api")
driver.element('xpath', "/html/body/div[1]/div/main/div[2]/div[2]/div/div/div[2]/div/button")[0].click()
driver.element('xpath', '/html/body/div[1]/div/main/div[2]/div[2]/div/div[2]/section/div[2]/button')[0].click()
File(
    name = 'mods/Fabric API.jar',
    url = driver.element('xpath', '/html/body/div[1]/div/main/div/div[2]/div[2]/div/p/a')[0].get_attribute('href'),
    version = 'java'
)

driver.close()
