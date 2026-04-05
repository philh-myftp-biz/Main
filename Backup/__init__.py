
# Force Verbose Mode
import sys
sys.argv += ['-v']

from philh_myftp_biz.web.ftp import FTP
from philh_myftp_biz.file import YAML
from philh_myftp_biz.pc import loc
from os import getpid

# Store PID
with loc.cache.child('PID.txt').open('w') as f:
    f.write(str(getpid()))

# Read configuration
config = YAML(loc.script.child('config.yaml')).read()

# Connect to the FTP server
ftp = FTP(
    host = 'philh.myftp.biz',
    username = 'Administrator',
    password = config['password']
)
