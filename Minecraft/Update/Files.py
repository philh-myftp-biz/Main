from philh_myftp_biz.web import download, Driver
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.file import temp
from philh_myftp_biz.text import hex
from philh_myftp_biz.pc import Path
from philh_myftp_biz import VERBOSE

#========================================================================

class Files(dict[str, Path]):
    
    def __setitem__(self,
        name: str,
        url: str
    ):
        
        Log.VERB(f'Found Link: {NAME=} | {URL=}')

        path = temp(
            name = hex.encode(name)
        )

        download(url, path)

        Log.INFO(f'Cached File: {NAME=}')

        super().__setitem__(name, path)

#========================================================================
# INIT

Log.INFO('Initializing File Discovery')

# Create new webdriver
driver = Driver(headless=(not VERBOSE))

# List of java files
java = Files()

# List of bedrock files
bedrock = Files()

#========================================================================
# JAVA - Geyser

NAME = 'mods/Geyser.jar'
URL = 'https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/fabric'

java[NAME] = URL

#========================================================================
# JAVA - Fabric Server

NAME = 'fabric-server-launch.jar'

# Get Fabric Server Launcher
driver.open('https://fabricmc.net/use/server/')

# Save the Fabric Server URL
URL = driver.element('xpath', '/html/body/main/div/article/div/div[1]/main/div[1]/div[4]/a')[0].get_attribute('href')

java[NAME] = URL

#========================================================================
# JAVA - Floodgate

NAME = 'mods/Floodgate.jar'

# Open the download page for the latest version
driver.open("https://modrinth.com/mod/floodgate/versions?l=fabric&c=release")

# Save the Floodgate URL 
URL = driver.element('xpath', "/html/body/div[1]/div[4]/main/div[5]/div[6]/div[3]/section/div[2]/div[3]/div[2]/div[1]/a")[0].get_attribute('href')

java[NAME] = URL

#========================================================================
# JAVA - Fabric API

NAME = 'mods/Fabric API.jar'

# Open the download page for the latest version
driver.open("https://modrinth.com/mod/fabric-api/versions?c=release")

# Save the download URL 
URL = driver.element('xpath', "/html/body/div[1]/div[4]/main/div[5]/div[6]/div[3]/section/div[2]/div[3]/div[2]/div[1]/a")[0].get_attribute('href')

java[NAME] = URL

#========================================================================

# Close the webdriver
driver.close()