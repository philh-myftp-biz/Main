from philh_myftp_biz.web import api, Driver
from philh_myftp_biz.modules import Module
from philh_myftp_biz.pc import ProgressBar
from philh_myftp_biz import ParsedArgs
from philh_myftp_biz.file import TXT

#==============================================
# Plex Module

# Declare the 'Plex' module
this = Module('E:/Plex')

# Store for execution pid
PIDstore = TXT(this.dir.child('/Torrenting/__pycache__/PID.txt'))

#==============================================
# Parse commandline arguements
args = ParsedArgs()

args.Arg(
    name = 'filter',
    default = '',
    desc = 'Only download items whose title contains this',
    handler = lambda x: x.lower()
)

#==============================================

# Create a progress bar
pbar = ProgressBar(0)

#==============================================
# VM module

# Declare the 'Virtual Machines' module
VM = Module('E:/Virtual Machines')

# Power on the Virtual Machine
VM.runH(
    'start', 'Torrenting'
)

#==============================================

# Create a new Webdriver
driver = Driver(
    headless = (not args['verbose']),
    debug = args['verbose'],
    extensions = [
        'https://addons.mozilla.org/firefox/downloads/file/4619486/adguard_adblocker-5.2.113.0.xpi' # AdBlocker
    ],
    fast_load = True
)

#==============================================
# qBitTorrent

host = None

while host is None:
    host = VM.cap('IP', 'Torrenting')

# Connect to the qbittorrent web interface on the 'Torrenting' Virtual Machine
qbit = api.qBitTorrent(
    host = host,
    username = 'admin',
    password = 'Torrenting123!',
    debug = args['verbose']
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