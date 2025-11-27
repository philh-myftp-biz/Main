from philh_myftp_biz.web import api, Driver
from philh_myftp_biz.modules import Module
from philh_myftp_biz import ParsedArgs

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
    handler = lambda x: [int(y) for y in x.split(',')]
)

args.Arg(
    name = 'debug',
    default = '',
    desc = 'Comma-Separated list of Debug Information to show (driver,qbit,vm,scanner)',
    handler = lambda x: x.split(',')
)

args.Arg(
    name = 'type',
    default = 'movie,show',
    desc = 'Comma-Separated list of media types to download (movie,show)',
    handler = lambda x: x.split(',')
)

#==============================================

# Declare the 'Virtual Machines' module
VM = Module('E:/Virtual Machines')

# Power on the Virtual Machine
VM.run(
    'start', 'Torrenting',
    hide = ('vm' not in args['debug'])
)

# Declare the 'Plex' module
this = Module('E:/Plex')

# Connect to the qbittorrent web interface on the 'Torrenting' Virtual Machine
qbit = api.qBitTorrent(
    host = VM.run('IP', 'Torrenting', hide=True).output('json'),
    username = 'admin',
    password = 'Torrenting123!',
    debug = ('qbit' in args['debug'])
)

# Connect to 'thepiratebay.org'
tpb = api.thePirateBay()

# Connect to 'omdbapi.com'
omdb = api.omdb()

# Create a new Webdriver
driver = Driver(
    debug = ('driver' in args['debug'])
)
