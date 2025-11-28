from philh_myftp_biz.web import api, Driver
from philh_myftp_biz.modules import Module
from philh_myftp_biz import ParsedArgs
from philh_myftp_biz.text import auto_convert

#==============================================
args = ParsedArgs()

args.Arg(
    name = 'limit',
    default = '100',
    desc = 'Maximum # of torrents to download',
    handler = int
)

args.Arg(
    name = 'filter',
    default = '',
    desc = 'Only download items whose title contains this',
    handler = lambda x: x.lower()
)

args.Arg(
    name = 'seeders',
    default = '15',
    desc = 'Minimum # of seeders per torrent',
    handler = int
)

args.Arg(
    name = 'quality',
    default = '720,1080',
    desc = 'Comma-Separated list of allowed qualities',
    handler = lambda x: [auto_convert(y) for y in x.split(',')]
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

# Create a new Webdriver
driver = Driver(
    headless = (not args['verbose']),
    debug = args['verbose'],
    extensions = ['adblock']
)

# Connect to the qbittorrent web interface on the 'Torrenting' Virtual Machine
qbit = api.qBitTorrent(
    host = VM.run('IP', 'Torrenting', hide=True).output('json'),
    username = 'admin',
    password = 'Torrenting123!',
    debug = args['verbose']
)

# Connect to 'thepiratebay.org'
tpb = api.thePirateBay(
    driver = driver,
    qbit = qbit
)

# Connect to 'omdbapi.com'
omdb = api.omdb()