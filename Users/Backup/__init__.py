from philh_myftp_biz.pc import script_dir, cache_dir, Path
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

local = Path('E:/Users/philh/')

def get_paths():
    
    for user in ftp.Path('/E/Users/philh/').children:

        if user.name == 'Administrator':
            continue

        for src in user.descendants:
            
            if src.is_file:
                
                yield (
                    src, 
                    local.child(src.path.replace('/E/Users/philh/', '', 1))
                )
