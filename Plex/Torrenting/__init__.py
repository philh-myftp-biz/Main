
from philh_myftp_biz.web.torrent import thePirateBay, qBitTorrent
from philh_myftp_biz.terminal import ParsedArgs
from philh_myftp_biz.web.driver import Driver
from philh_myftp_biz.modules import Module
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.array import List
from philh_myftp_biz.file import JSON
from philh_myftp_biz import VERBOSE

from json.decoder import JSONDecodeError
from os import getpid

#==============================================
# Modules

this = Module('E:/Plex/')

VM = Module('E:/Virtual Machines/')

#==============================================
# PID

PIDstore: List[str] = List(JSON(this.child('/Torrenting/__pycache__/PID.json')))

PIDstore.save([f'python-{getpid()}'])

#==============================================
# Parse commandline arguements

ParsedArgs.Arg(
    name = 'filter',
    default = '',
    desc = 'Only download items whose title contains this',
    handler = lambda x: x.split('|')
)

ParsedArgs.Arg(
    name = 'limit',
    default = 100,
    desc = 'Maximum # of items to download',
    handler = int
)

ParsedArgs.Arg(
    name = 'timeout',
    default = 300, # 5 minutes
    desc = '# of seconds to wait before timing out',
    handler = int
)

#==============================================
# WEBDRIVER

driver = Driver(
    headless = (not ParsedArgs['verbose']),
    eager = True
)

for pid in driver.Task.PIDs:
    PIDstore += f'firefox-{pid}'

#==============================================
# qBitTorrent

# Start the Virtual Machine
VM.runH('Start', 'Torrenting')

host: str|None = None

Log.VERB(
    f'Discovering VM\n'+ \
    f"name='Torrenting'"
)

VERBOSE.pause()

# Loop until an IP address has been found
while host is None:

    try:
        host = VM.cap('IP', 'Torrenting')
    except JSONDecodeError:
        pass

VERBOSE.resume()

Log.VERB(
    f'Discovering VM\n'+ \
    f"name='Torrenting'\n"+ \
    f"{host=}"
)

# Connect to the qbittorrent web interface on the 'Torrenting' Virtual Machine
qbit = qBitTorrent(
    host = host,
    username = 'admin',
    password = 'Torrenting123!',
    timeout = ParsedArgs['timeout']
)

#==============================================
# thePirateBay

thePirateBay.driver = driver
thePirateBay.qbit = qbit

#==============================================