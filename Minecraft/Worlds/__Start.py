from philh_myftp_biz.process import Start, SubProcess
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.file import YAML
from philh_myftp_biz.web import Port
from __init__ import Worlds, Tasks

processes: list[SubProcess] = []

#========================================================================================================

for w in Worlds():

    #====================================================

    NAME = w.name()

    config = YAML(w.child('config.yaml')).read()

    #====================================================

    Ports = [
        Port(config['port']['java']),
        Port(config['port']['bedrock'])
    ]

    if any([p.listening for p in Ports]):
        
        Log.FAIL(f'Port Failure: {NAME=} {Ports[0]} | {Ports[1]}')
        
        continue

    #====================================================

    #
    match config['edition']:

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
    process = Start(
        args = args,
        dir = w.path
    )

    while process._task is None:
        pass
    
    Tasks[w.name()] = process._task

    processes += [process]

#========================================================================================================

# Wait for all subprocesses to complete
for process in processes:
    process.wait()
