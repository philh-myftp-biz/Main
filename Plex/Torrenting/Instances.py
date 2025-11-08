from philh_myftp_biz.web import api, Driver
from philh_myftp_biz.modules import Module
from philh_myftp_biz.pc import Path

# Declare the 'Plex' module
this = Module('E:/Plex')

# Declare the temporary directory for downloads
temp = Path('E:/Users/philh/Torrenting/Downloads/')

# Declare the 'Virtual Machines' module
VM = Module('E:/Virtual Machines')

# Connect to the qbittorrent web interface on the 'Torrenting' Virtual Machine
qbit = api.qBitTorrent(
    host = VM.run('IP', 'Torrenting', hide=True).output('json'),
    username = 'admin',
    password = 'Torrenting123!'
)

# Connect to 'thepiratebay.org'
tpb = api.thePirateBay()

# Connect to 'omdbapi.com'
omdb = api.omdb()

# Create a new Webdriver
driver = Driver(debug=True)