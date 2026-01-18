from philh_myftp_biz.terminal import ParsedArgs
from philh_myftp_biz.web import api, Driver
from philh_myftp_biz.modules import Module
from json.decoder import JSONDecodeError
from os import getpid

#==============================================
# Plex Module

# Declare the 'Plex' module
this = Module('E:/Plex')

#==============================================
# PID

with this.dir.child('/Torrenting/__pycache__/PID.txt').open('w') as txt:
    txt.write( str(getpid()) )

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
    name = 'seeders',
    default = 15,
    desc = 'Minimum # of seeders for torrents',
    handler = int
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
# VM module

# Declare the 'Virtual Machines' module
VM = Module('E:/Virtual Machines')

VM.runH('start', 'Torrenting')

#==============================================

# Create a new Webdriver
driver = Driver(
    headless = (not args['verbose']),
    debug = args['verbose'],
    fast_load = True
)

#==============================================
# qBitTorrent

host = None

while host is None:
    
    if args['verbose']:
        print('Contacting Virtual Machine ...')
    
    try:
        host = VM.cap('IP', 'Torrenting')
    except JSONDecodeError:
        pass

# Connect to the qbittorrent web interface on the 'Torrenting' Virtual Machine
qbit = api.qBitTorrent(
    host = host,
    username = 'admin',
    password = 'Torrenting123!',
    debug = args['verbose'],
    timeout = args['timeout']
)

#==============================================
# thePirateBay

# Connect to 'thepiratebay.org'
tpb = api.thePirateBay(
    driver = driver,
    qbit = qbit
)

#==============================================
# omdb

# Connect to 'omdbapi.com'
omdb = api.omdb(
    debug = args['verbose']
)

#==============================================