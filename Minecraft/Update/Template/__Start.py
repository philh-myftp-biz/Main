from philh_myftp_biz.file import TXT
from philh_myftp_biz.pc import cwd
from philh_myftp_biz import run

dir = cwd()

PIDstore = TXT(dir.child('/.PID.txt'))

# ====================================================

args = None

for p in dir.children():

    # If server is Java Edition
    if p.ext() == 'jar':
        args = [
            'java', 
            '-Xmx2G',
            '-jar', 'fabric-server-launch.jar',
            'nogui'
        ]
        break

    # If server is Bedrock Edition
    elif p.ext() == 'exe':
        args = []
        break

# ====================================================

if args:

    #
    r = run(
        args = args,
        dir = dir
    )

    PID: int = next(r.PIDs(), None)

    if PID:

        PIDstore.save(PID)
