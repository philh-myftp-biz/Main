from __init__ import File
from philh_myftp_biz.web import Driver

# Create new webdriver
driver = Driver()

# List of java files
java: list[File] = []

# List of bedrock files
bedrock: list[File] = []

# Get Geyser Mod
java += [File(
    name = 'mods/Geyser.jar',
    url = 'https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/fabric'
)]

# Get Fabric Server Launcher
driver.open('https://fabricmc.net/use/server/')
java += [File(
    name = 'fabric-server-launch.jar',
    url = driver.element('xpath', '/html/body/main/div/article/div/div[1]/main/div[1]/div[4]/a')[0].get_attribute('href')
)]

# Get Floodgate Mod
driver.open("https://modrinth.com/mod/floodgate/versions?l=fabric")
java += [File(
    name = 'mods/Floodgate.jar',
    url = driver.element('xpath', "/html/body/div[1]/div[4]/main/div[5]/div[6]/div[3]/section/div[2]/div[3]/div[2]/div[1]/a")[0].get_attribute('href')
)]

# Get Fabric API
driver.open("https://www.curseforge.com/minecraft/mc-mods/fabric-api")
driver.element('xpath', "/html/body/div[1]/div/main/div[2]/div[2]/div/div/div[2]/div/button")[0].click()
driver.element('xpath', '/html/body/div[1]/div/main/div[2]/div[2]/div/div[2]/section/div[2]/button')[0].click()
java += [File(
    name = 'mods/Fabric API.jar',
    url = driver.element('xpath', '/html/body/div[1]/div/main/div/div[2]/div[2]/div/p/a')[0].get_attribute('href')
)]

# Close the webdriver
driver.close()