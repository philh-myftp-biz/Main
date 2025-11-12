import urllib.request
from philswebsite import site
import os, time, urllib

wait_hours = 5

def getFiles():
    files = { 'Java' : [], 'Bedrock' : [] }
    browser, By = site.web.browser.start(), site.web.browser.By

    files['Java'].append(['mods/Geyser.jar', 'https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/fabric'])

    browser.get('https://fabricmc.net/use/server/')
    url = browser.find_element(By.XPATH, '/html/body/main/div/article/div/div[1]/main/div[1]/div[4]/a').get_attribute('href')
    files['Java'].append(['fabric-server-launch.jar', url])

    browser.get("https://modrinth.com/mod/floodgate/versions?l=fabric")
    url = browser.find_element(By.XPATH, "/html/body/div[1]/div[4]/main/div[5]/div[6]/div[3]/section/div[2]/div[3]/div[2]/div[1]/a").get_attribute('href')
    files['Java'].append(['mods/Floodgate.jar', url])

    browser.get("https://www.curseforge.com/minecraft/mc-mods/fabric-api")
    browser.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/div[2]/div/div/div[2]/div/button").click()
    browser.find_element(By.XPATH, '/html/body/div[1]/div/main/div[2]/div[2]/div/div[2]/section/div[2]/button').click()
    url = browser.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[2]/div[2]/div/p/a').get_attribute('href')
    files['Java'].append(['mods/Fabric API.jar', url])

    browser.close()
    return files

processes = []

while True:
    for file in site.dir.getChildren('G:/Servers/Minecraft/Servers/', False):
        files = getFiles()
        server = file.split('/')[-2]
        dir = f'G:/Servers/Minecraft/Servers/{server}'
        edition = site.file.text(dir+'/Edition.ini').read()
        
        if edition == 'Java':
            os.chdir(dir)
            for item in site.dir.getChildren('Server', Folder=False):
                if not (site.file.ext(item) in ['json', 'properties', 'txt']): os.remove(item)

            for folder in ['logs', 'libraries', '.fabric', 'versions']:
                os.remove({folder})

            for path, url in files['Java']:
                urllib.request.urlretrieve(url, path)

            processes.append(site.run(['java', '-Xmx2G', '-jar', 'fabric-server-launch.jar', 'nogui'], dir='Server'))

    time.sleep(30)#wait_hours*3600)
    
    for process in processes: process.stop()
    processes = []