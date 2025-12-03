from __init__ import args, Servers, Edition
from philh_myftp_biz import run

#
for server in Servers():

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
