from philh_myftp_biz.process import Start
from philh_myftp_biz.file import YAML
from __init__ import Worlds, Tasks

for w in Worlds():

    #
    match YAML(w.child('config.yaml')).read()['edition']:

        #
        case 'java':
            args = [
                'java', 
                '-Xmx2G',
                '-jar', 'fabric-server-launch.jar',
                'nogui'
            ]

        #
        case 'bedrock':
            args = []

    #====================================================

    #
    r = Start(
        args = args,
        dir = w.path
    )

    Tasks[w.name()] = r._task
