from philh_myftp_biz.terminal import ParsedArgs
from philh_myftp_biz.web import api, Driver
from philh_myftp_biz.modules import Module
from json.decoder import JSONDecodeError
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.array import List
from philh_myftp_biz.file import JSON
from os import getpid

#==============================================
# Plex Module

# Declare the 'Plex' module
this = Module('E:/Plex')

#==============================================
# PID

#
PIDstore: List[str] = List(JSON(this.dir.child('/Torrenting/__pycache__/PID.json')))

# Clear the PID store
PIDstore.save([f'python-{getpid()}'])

#==============================================
# Parse commandline arguements
args = ParsedArgs()

args.Arg(
    name = 'filter',
    default = '',
    desc = 'Only download items whose title contains this',
    handler = lambda x: x.lower()
)

args.Arg(
    name = 'limit',
    default = 100,
    desc = 'Maximum # of items to download',
    handler = int
)

args.Arg(
    name = 'timeout',
    default = 300, # 5 minutes
    desc = '# of seconds to wait before timing out',
    handler = int
)

#==============================================
# WEBDRIVER

driver = Driver(
    headless = (not args['verbose']),
    fast_load = True
)

#
for pid in driver.Task.PIDs():
    PIDstore += f'firefox-{pid}'

#==============================================
# qBitTorrent

# Declare the 'Virtual Machines' module
VM = Module('E:/Virtual Machines')

#
VM.runH('start', 'Torrenting')

#
host = None

#
while host is None:
    
    Log.VERB("Discovering VM: (name='Torrenting')")
    
    try:
        host = VM.cap('IP', 'Torrenting')
    except JSONDecodeError:
        pass

Log.INFO(f"Discovered VM: (name='Torrenting', {host=})")

# Connect to the qbittorrent web interface on the 'Torrenting' Virtual Machine
qbit = api.qBitTorrent(
    host = host,
    username = 'admin',
    password = 'Torrenting123!',
    timeout = args['timeout']
)

#==============================================
# thePirateBay

# Connect to 'thepiratebay.org'
tpb = api.thePirateBay(
    url = 'thepiratebay11.com',
    driver = driver,
    qbit = qbit
)

#==============================================
# omdb

# Connect to 'omdbapi.com'
omdb = api.omdb()

#==============================================