from philh_myftp_biz.modules import Module, ModuleLockedError
from philh_myftp_biz.web import api, Driver
from philh_myftp_biz import ParsedArgs
from philh_myftp_biz.pc import ProgressBar

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
# Plex Module

# Declare the 'Plex' module
this = Module('E:/Plex')

# If the Plex module is locked
if this.lock.locked():
    # Raise Error
    raise ModuleLockedError(this)

else:
    # Lock the Plex module
    this.lock.lock()

#==============================================
# VM module

# Declare the 'Virtual Machines' module
VM = Module('E:/Virtual Machines')

# Power on the Virtual Machine
VM.run(
    'start', 'Torrenting',
    hide = (not args['verbose'])
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
    host = VM.run('IP', 'Torrenting', hide=True).output('json')

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