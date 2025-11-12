from __init__ import files

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