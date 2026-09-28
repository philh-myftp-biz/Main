from philh_myftp_biz.web.torrent import thePirateBay, qBitTorrent
from philh_myftp_biz.terminal import Args, Log
from philh_myftp_biz.web.driver import Driver
from philh_myftp_biz.modules import Module
from json.decoder import JSONDecodeError
from philh_myftp_biz.pc import Path
from os import getpid

#==============================================

VM = Module('E:/Virtual Machines/')

PIDstore = Path('E:/Plex/Torrenting/__pycache__/PID.json').JSON.List
PIDstore.save([f'python-{getpid()}'])

#==============================================

Args.Arg(
    name = 'filter',
    default = [''],
    desc = 'Only download items whose title contains this',
    handler = lambda x: x.split(',')
)

Args.Arg(
    name = 'limit',
    default = 100,
    desc = 'Maximum # of items to download',
    handler = int
)

Args.Arg(
    name = 'timeout',
    default = 300, # 5 minutes
    desc = '# of seconds to wait before timing out',
    handler = int
)

#==============================================

VM.runH('Start', 'Torrenting')

Log.VERB(f"Discovering VM\nname='Torrenting'")

while True:
    try: 
        qBitTorrent.connect(
            host = VM.cap('IP', 'Torrenting'),
            username = 'admin',
            password = 'Torrenting123!',
            timeout = Args['timeout']
        )
        break
    except (JSONDecodeError, ConnectionError): 
        pass

#==============================================

driver = Driver(
    headless = (not Args['verbose']),
    eager = True
)

for pid in driver.Task.PIDs:
    PIDstore += f'firefox-{pid}'

thePirateBay.driver = driver

#==============================================