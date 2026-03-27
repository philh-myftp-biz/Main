
# Force Verbose Mode
import sys
sys.argv += ['-v']

from philh_myftp_biz.pc import script_dir, cache_dir
from philh_myftp_biz.remotepc.ftp import FTP
from philh_myftp_biz.file import YAML
from os import getpid

# Store PID
with cache_dir().child('PID.txt').open('w') as f:
    f.write(str(getpid()))

# Read configuration
config = YAML(script_dir().child('config.yaml')).read()

# Connect to the FTP server
ftp = FTP(
    host = 'philh.myftp.biz',
    username = 'Administrator',
    password = config['password']
)
