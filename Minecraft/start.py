from __init__ import args, Worlds, Edition
from philh_myftp_biz import run

#
for server in Worlds():

    edit = Edition(server)

    # If server is Java Edition
    if edit == 'java':
        args = [
            'java', 
            '-Xmx2G',
            '-jar', 'fabric-server-launch.jar',
            'nogui'
        ]
        
    # If server is Bedrock Edition
    elif edit == 'bedrock':
        args = []

    #
    run(
        args,
        dir = server.path
    )
