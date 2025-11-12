from philh_myftp_biz import Args, run
from __init__ import Server, this

args = Args()

servers: list[Server] = []

if len(args) == 1:
    
    servers += [Server(
        path = this.dir.child(f'/Worlds/{args[0]}')
    )]

else:

    for p in this.dir.child('/Worlds/'):
        servers += [Server(p)]

for server in servers:

    if server.edition == 'java':

        run(
            args = [
                'java', 
                '-Xmx2G',
                '-jar', 'fabric-server-launch.jar',
                'nogui'
            ],
            dir = server.path
        )