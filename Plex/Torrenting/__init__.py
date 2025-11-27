from philh_myftp_biz.web import api, Driver
from philh_myftp_biz.modules import Module
from philh_myftp_biz import ParsedArgs

#==============================================
args = ParsedArgs()

args.Arg(
    name = 'limit',
    default = 100,
    desc = 'Maximum # of torrents to download',
    handler = int
)

args.Arg(
    name = 'filter',
    default = '',
    desc = 'Only download items whose title contains this',
    handler = lambda x: x.lower()
)

#==============================================

# Declare the 'Virtual Machines' module
VM = Module('E:/Virtual Machines')

# Power on the Virtual Machine
VM.run(
    'start', 'Torrenting',
    hide = (not args['verbose'])
)

# Declare the 'Plex' module
this = Module('E:/Plex')

# Connect to the qbittorrent web interface on the 'Torrenting' Virtual Machine
qbit = api.qBitTorrent(
    host = VM.run('IP', 'Torrenting', hide=True).output('json'),
    username = 'admin',
    password = 'Torrenting123!',
    debug = args['verbose']
)

# Connect to 'thepiratebay.org'
tpb = api.thePirateBay()

# Connect to 'omdbapi.com'
omdb = api.omdb()

# Create a new Webdriver
driver = Driver(
    debug = args['verbose']
)
